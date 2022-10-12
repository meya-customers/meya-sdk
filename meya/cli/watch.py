from pathspec import PathSpec
from watchdog.utils import stat
from watchdog.utils.dirsnapshot import DirectorySnapshot


def patch_watchdog(ignore_spec: PathSpec):
    # TODO Submit Watchdog and Hachiko and pytest-watch PRs instead of monkey-patching

    def custom_stat(path):
        if ignore_spec.match_file(path):
            return stat("/dev/null")
        else:
            return stat(path)

    def custom_directory_snapshot(path, recursive=True):
        return DirectorySnapshot(path, recursive, stat=custom_stat)

    try:
        from watchdog.observers import fsevents
    except ImportError:
        # Not Mac, no patch needed
        return

    fsevents.DirectorySnapshot = custom_directory_snapshot
