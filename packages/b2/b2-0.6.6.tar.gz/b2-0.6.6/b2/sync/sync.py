######################################################################
#
# File: b2/sync/sync.py
#
# Copyright 2016 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

from __future__ import division

import re
import six

from ..exception import CommandError
from .policy_manager import POLICY_MANAGER
from .report import SyncReport

try:
    import concurrent.futures as futures
except ImportError:
    import futures


def next_or_none(iterator):
    """
    Returns the next item from the iterator, or None if there are no more.
    """
    try:
        return six.advance_iterator(iterator)
    except StopIteration:
        return None


def zip_folders(folder_a, folder_b, reporter, exclusions=tuple()):
    """
    An iterator over all of the files in the union of two folders,
    matching file names.

    Each item is a pair (file_a, file_b) with the corresponding file
    in both folders.  Either file (but not both) will be None if the
    file is in only one folder.
    :param folder_a: A Folder object.
    :param folder_b: A Folder object.
    """

    iter_a = (
        f for f in folder_a.all_files(reporter) if not any(ex.match(f.name) for ex in exclusions)
    )
    iter_b = folder_b.all_files(reporter)

    current_a = next_or_none(iter_a)
    current_b = next_or_none(iter_b)
    while current_a is not None or current_b is not None:
        if current_a is None:
            yield (None, current_b)
            current_b = next_or_none(iter_b)
        elif current_b is None:
            yield (current_a, None)
            current_a = next_or_none(iter_a)
        elif current_a.name < current_b.name:
            yield (current_a, None)
            current_a = next_or_none(iter_a)
        elif current_b.name < current_a.name:
            yield (None, current_b)
            current_b = next_or_none(iter_b)
        else:
            assert current_a.name == current_b.name
            yield (current_a, current_b)
            current_a = next_or_none(iter_a)
            current_b = next_or_none(iter_b)


def make_file_sync_actions(
    sync_type, source_file, dest_file, source_folder, dest_folder, args, now_millis
):
    """
    Yields the sequence of actions needed to sync the two files
    """

    policy = POLICY_MANAGER.get_policy(
        sync_type, source_file, source_folder, dest_file, dest_folder, now_millis, args
    )
    for action in policy.get_all_actions():
        yield action


def make_folder_sync_actions(source_folder, dest_folder, args, now_millis, reporter):
    """
    Yields a sequence of actions that will sync the destination
    folder to the source folder.
    """
    if args.skipNewer and args.replaceNewer:
        raise CommandError('--skipNewer and --replaceNewer are incompatible')

    if args.delete and (args.keepDays is not None):
        raise CommandError('--delete and --keepDays are incompatible')

    if (args.keepDays is not None) and (dest_folder.folder_type() == 'local'):
        raise CommandError('--keepDays cannot be used for local files')

    exclusions = [re.compile(ex) for ex in args.excludeRegex]

    source_type = source_folder.folder_type()
    dest_type = dest_folder.folder_type()
    sync_type = '%s-to-%s' % (source_type, dest_type)
    if (source_folder.folder_type(), dest_folder.folder_type()) not in [
        ('b2', 'local'), ('local', 'b2')
    ]:
        raise NotImplementedError("Sync support only local-to-b2 and b2-to-local")
    for (source_file, dest_file) in zip_folders(source_folder, dest_folder, reporter, exclusions):
        if source_folder.folder_type() == 'local':
            if source_file is not None:
                reporter.update_compare(1)
        else:
            if dest_file is not None:
                reporter.update_compare(1)
        for action in make_file_sync_actions(
            sync_type, source_file, dest_file, source_folder, dest_folder, args, now_millis
        ):
            yield action


def count_files(local_folder, reporter):
    """
    Counts all of the files in a local folder.
    """
    # Don't pass in a reporter to all_files.  Broken symlinks will be reported
    # during the next pass when the source and dest files are compared.
    for _ in local_folder.all_files(None):
        reporter.update_local(1)
    reporter.end_local()


def sync_folders(source_folder, dest_folder, args, now_millis, stdout, no_progress, max_workers):
    """
    Syncs two folders.  Always ensures that every file in the
    source is also in the destination.  Deletes any file versions
    in the destination older than history_days.
    """

    # For downloads, make sure that the target directory is there.
    if dest_folder.folder_type() == 'local':
        dest_folder.ensure_present()

    # Make a reporter to report progress.
    with SyncReport(stdout, no_progress) as reporter:

        # Make an executor to count files and run all of the actions.  This is
        # not the same as the executor in the API object, which is used for
        # uploads.  The tasks in this executor wait for uploads.  Putting them
        # in the same thread pool could lead to deadlock.
        sync_executor = futures.ThreadPoolExecutor(max_workers=max_workers)

        # First, start the thread that counts the local files.  That's the operation
        # that should be fastest, and it provides scale for the progress reporting.
        local_folder = None
        if source_folder.folder_type() == 'local':
            local_folder = source_folder
        if dest_folder.folder_type() == 'local':
            local_folder = dest_folder
        if local_folder is None:
            raise ValueError('neither folder is a local folder')
        sync_executor.submit(count_files, local_folder, reporter)

        # Schedule each of the actions
        bucket = None
        if source_folder.folder_type() == 'b2':
            bucket = source_folder.bucket
        if dest_folder.folder_type() == 'b2':
            bucket = dest_folder.bucket
        if bucket is None:
            raise ValueError('neither folder is a b2 folder')
        action_futures = []
        total_files = 0
        total_bytes = 0
        for action in make_folder_sync_actions(
            source_folder, dest_folder, args, now_millis, reporter
        ):
            future = sync_executor.submit(action.run, bucket, reporter)
            action_futures.append(future)
            total_files += 1
            total_bytes += action.get_bytes()
        reporter.end_compare(total_files, total_bytes)

        # Wait for everything to finish
        sync_executor.shutdown()
        if any(1 for f in action_futures if f.exception() is not None):
            raise CommandError('sync is incomplete')
