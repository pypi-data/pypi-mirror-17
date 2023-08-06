import os
import sys
import time

from click import echo, group, argument, option, UsageError, ClickException

from homely._errors import RepoError, JsonError
from homely._utils import RepoListConfig, saveconfig, RepoInfo, mkcfgdir
from homely._ui import (
    run_update, addfromremote, yesno,
    setverbose, setinteractive, setfragile, setallowpull,
    isinteractive, warning, note
)
from homely._vcs import getrepohandler


CMD = os.path.basename(sys.argv[0])


class Fatal(Exception):
    pass


def _globals(verbhelp=None):
    if verbhelp is None:
        verbhelp = "Product extra output"

    # return a decorator function
    def _decorator(command):
        def proxy(verbose, fragile, interactive, **kwargs):
            # handle the --verbose, --fragile and --interactive options
            setverbose(verbose)
            setinteractive(interactive)
            setfragile(fragile)
            # pass all other arguments on to the command
            command(**kwargs)
        proxy.__name__ = command.__name__
        proxy.__doc__ = command.__doc__
        proxy = option('--interactive/--no-interactive', default=True,
                       help="Prompt user for input? Use --no-interactive in"
                       " scripts where a tty will not be connected")(proxy)
        proxy = option('--fragile', is_flag=True, help="homely will exit(1)"
                       " whenever a Warning is generated")(proxy)
        proxy = option('-v', '--verbose', 'verbose', is_flag=True,
                       help=verbhelp)(proxy)
        return proxy
    return _decorator


@group()
def homely():
    """
    Single-command dotfile installation.
    """
    pass


@homely.command()
# FIXME: add the ability to install multiple things at once
@argument('repo_path')
@argument('dest_path', required=False)
@_globals()
def add(repo_path, dest_path):
    '''
    Install a new repo on your system
    '''
    repo = getrepohandler(repo_path)
    if not repo:
        raise ClickException("No handler for repo at %s" % repo_path)

    # if the repo isn't on disk yet, we'll need to make a local clone of it
    if repo.isremote:
        localrepo, needpull = addfromremote(repo, dest_path)
    elif dest_path:
        raise UsageError("DEST_PATH is only for repos hosted online")
    else:
        needpull = False
        localrepo = RepoInfo(
            repo,
            repo.getrepoid(),
            None,
        )

    # if we don't have a local repo, then there is nothing more to do
    if not localrepo:
        return

    # remember this new local repo
    with saveconfig(RepoListConfig()) as cfg:
        cfg.add_repo(localrepo)
    success = run_update([localrepo],
                         pullfirst=needpull,
                         cancleanup=True)
    if not success:
        sys.exit(1)


@homely.command()
@option('--format', '-f',
        help="Format string for the output, which will be passed through"
        " str.format(). You may use the following named replacements:"
        "\n%(repoid)s"
        "\n%(localpath)s"
        "\n%(canonical)s")
def repolist(format):
    cfg = RepoListConfig()
    for info in cfg.find_all():
        vars_ = dict(
            repoid=info.repoid,
            localpath=info.localrepo.repo_path,
            canonical=(info.canonicalrepo.repo_path
                       if info.canonicalrepo else '')
        )
        print(format % vars_)


@homely.command()
@argument('identifier', nargs=-1)
@option('--force', '-f', is_flag=True,
        help="Do not ask the user for confirmation before removing a repo that"
        " still exists on disk. You must use --force if you have also used"
        " --no-interactive.")
@option('--update', '-u', is_flag=True,
        help="Perform update/cleanup of all repos after removal.")
def remove(identifier, force, update):
    '''
    Remove repo identified by IDENTIFIER. IDENTIFIER can be a path to a repo or
    a commit hash or a canonical url.
    '''
    errors = False
    removed = False
    for one in identifier:
        cfg = RepoListConfig()
        info = cfg.find_by_any(one, "ilc")
        if not info:
            warning("No repos matching %r" % one)
            errors = True
            continue

        # if the local repo still exists, then we need to prompt if the user
        # hasn't used force mode
        if os.path.isdir(info.localrepo.repo_path) and not force:
            if not isinteractive():
                warning(
                    "Use --force to remove a repo that still exists on disk")
                errors = True
                continue

            prompt = "Are you sure you want to remove repo [%s] %s?" % (
                info.localrepo.shortid(info.repoid), info.localrepo.repo_path)
            if not yesno(prompt, False):
                continue

        # update the config ...
        note("Removing record of repo [%s] at %s" % (
            info.shortid(), info.localrepo.repo_path))
        with saveconfig(RepoListConfig()) as cfg:
            cfg.remove_repo(info.repoid)
        removed = True

    # if there were errors, then don't try and do an update
    if errors:
        sys.exit(1)

    if not removed:
        return

    # ask the user if they would like to update everything now?
    if (not update) and isinteractive():
        prompt = ("Files created by old repos will not be removed until you"
                  " perform an update of all other repos. Would you like to "
                  " do this now?")
        update = yesno(prompt, None, True)

    if update:
        # run an update with all remaining repos
        all_repos = cfg.find_all()
        success = run_update(list(all_repos), pullfirst=True, cancleanup=True)
        if not success:
            sys.exit(1)


@homely.command()
@argument('identifiers', nargs=-1, metavar="REPO")
@option('--nopull', is_flag=True)
@option('--only', '-o', multiple=True,
        help="Only process the named sections (whole names only)")
@option('--assume', '-a', is_flag=True,
        help="Assume that previous answers to yes/no prompts are correct")
@_globals()
def update(identifiers, nopull, only, assume):
    '''
    Git pull the specified REPOs and then re-run them.

    Each REPO must be a repoid or localpath from
    ~/.homely/repos.json.
    '''
    if assume:
        setinteractive("ASSUME")
    setallowpull(not nopull)
    cfg = RepoListConfig()
    if len(identifiers):
        updatedict = {}
        for identifier in identifiers:
            repo = cfg.find_by_any(identifier, "ilc")
            if repo is None:
                hint = "Try running %s add /path/to/this/repo first" % CMD
                raise Fatal("Unrecognised repo %s (%s)" % (identifier, hint))
            updatedict[repo.repoid] = repo
        updatelist = updatedict.values()
        cleanup = len(updatelist) == cfg.repo_count()
    else:
        updatelist = list(cfg.find_all())
        cleanup = True
    success = run_update(updatelist,
                         pullfirst=not nopull,
                         only=only,
                         cancleanup=cleanup)
    if not success:
        sys.exit(1)


@homely.command()
@option('--pause', is_flag=True,
        help="Pause automatic updates. This can be useful while you are"
        " working on your HOMELY.py script")
@option('--unpause', is_flag=True, help="Un-pause automatic updates")
@option('--errorfile', is_flag=True,
        help="Prints the _path_ of the file containing the output of the"
        " previous 'homely update' run that was initiated by autoupdate.")
@option('--tmux', is_flag=True,
        help="Run 'homely update' in a new window in the current tmux session."
        " Exit code and output is the same as for 'homely updatestatus'")
@option('--daemon', is_flag=True,
        help="""Run 'homely update --assume --autono-interactive' in a daemon
        process. Daemon will not spawned unless sufficient time has elapsed
        since the last complete update (see --interval). Exit code and output
        is the same as for 'homely updatestatus'.""")
@option('--interval', type=int, default=60*60*6,
        help="How long to wait between updates.")
@_globals(verbhelp="Passed to 'homely updatestatus' when --tmux or --daemon"
          " options are used.")
def autoupdate(**kwargs):
    primary = 'pause', 'unpause', 'errorfile', 'tmux', 'daemon'
    action = None
    for name in primary:
        if kwargs[name]:
            if action is not None:
                raise UsageError("Can't combined --%s and --%s options"
                                 % (action, name))
            action = name

    if action is None:
        raise UsageError("Can't combined --%s and --%s options"
                         % (action, name))

    if action == 'pause':
        mkcfgdir()
        with open(os.environ['HOMELY_PAUSEFILE'], 'w') as f:
            f.write(time.strftime("%H:%M"))
        return

    if action == 'unpause':
        pausefile = os.environ['HOMELY_PAUSEFILE']
        if os.path.exists(pausefile):
            os.unlink(pausefile)
        return

    raise Exception("TODO: action %r" % action)  # noqa

    # TODO: ensure only one of the following can be used at any one time:
    # --errors
    # --tmux
    # TODO: the only option compatible with --timeout is --tmux
    # TODO: the only option compatible with --tmux is --timeout
    '''
    Interactively update all your repos on a regular basis.
    E.g., add this to your ~/.bashrc:

        homely autoupdate --weekly
    '''
    raise Exception("TODO: check timestamp in ~/.homely/last-check")  # noqa
    raise Exception("TODO: update all repos if necessary")  # noqa
    raise Exception("TODO: put new timestamp in ~/.homely/last-check")  # noqa


@homely.command()
@_globals(verbhelp="""The time of the previous status change will be printed to
          stdout in the format '%H:%M'. If 'homely update' is currently running
          then the name of the current section will also be included in the
          output.""")
def updatestatus():
    """
    Returns an exit code indicating the state of the current or previous
    'homely update' process. The exit code will be one of the following:
      0  ..  No 'homely update' process is running.
      2  ..  A 'homely update' process has never been run.
      3  ..  A 'homely update' process is currently running.
      4  ..  Updates using 'autoupdate' are currently paused.
      5  ..  The most recent update raised Warnings or failed altogether.
      1  ..  (An unexpected error occurred trying to get the status.)

    This command is designed to be fast enough to include in your $PS1 shell
    prompt or tmux statusline.
    """
    raise Exception("updatestatus not handled by shell script")  # noqa


@homely.command()
def repotest():
    '''
    Test REPO's HOMELY.py for errors.
    '''
    raise Exception("TODO: implement this")  # noqa


def main():
    try:
        # FIXME: always ensure git is installed first
        homely()
    except (Fatal, RepoError, JsonError) as err:
        echo("ERROR: %s" % err, err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
