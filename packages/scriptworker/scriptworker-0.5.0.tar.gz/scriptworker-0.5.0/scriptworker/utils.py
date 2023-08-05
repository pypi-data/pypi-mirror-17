#!/usr/bin/env python
"""Utils for scriptworker
"""
import aiohttp
import arrow
import asyncio
import functools
import hashlib
import json
import logging
import os
import shutil
from taskcluster.utils import calculateSleepTime
from taskcluster.client import createTemporaryCredentials
from scriptworker.exceptions import ScriptWorkerException, ScriptWorkerRetryException

log = logging.getLogger(__name__)


async def request(context, url, timeout=60, method='get', good=(200, ),
                  retry=tuple(range(500, 512)), return_type='text', **kwargs):
    """Async aiohttp request wrapper
    """
    session = context.session
    with aiohttp.Timeout(timeout):
        log.debug("{} {}".format(method.upper(), url))
        async with session.request(method, url, **kwargs) as resp:
            log.debug("Status {}".format(resp.status))
            message = "Bad status {}".format(resp.status)
            if resp.status in retry:
                raise ScriptWorkerRetryException(message)
            if resp.status not in good:
                raise ScriptWorkerException(message)
            if return_type == 'text':
                return await resp.text()
            elif return_type == 'json':
                return await resp.json()
            else:
                return resp


async def retry_request(*args, retry_exceptions=(ScriptWorkerRetryException, ),
                        **kwargs):
    """Retry the `request` function
    """
    return await retry_async(request, retry_exceptions=retry_exceptions,
                             args=args, kwargs=kwargs)


def datestring_to_timestamp(datestring):
    """ Create a timetamp from a taskcluster datestring
    datestring: a string in the form of "2016-04-16T03:46:24.958Z"
    """
    return arrow.get(datestring).timestamp


def to_unicode(line):
    """Avoid ``|b'line'|`` type messages in the logs
    """
    try:
        line = line.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        pass
    return line


def makedirs(path):
    """mkdir -p
    """
    if path and not os.path.exists(path):
        log.debug("makedirs({})".format(path))
        os.makedirs(path)


def cleanup(context):
    """Clean up the work_dir and artifact_dir between task runs.
    """
    for name in 'work_dir', 'artifact_dir', 'task_log_dir':
        path = context.config[name]
        if os.path.exists(path):
            log.debug("rmtree({})".format(path))
            shutil.rmtree(path)
        makedirs(path)


async def retry_async(func, attempts=5, sleeptime_callback=None,
                      retry_exceptions=(Exception, ), args=(), kwargs=None):
    """Retry `func`, where `func` is an awaitable.
    """
    kwargs = kwargs or {}
    sleeptime_callback = sleeptime_callback or calculateSleepTime
    attempt = 1
    while True:
        try:
            log.debug("retry_async: Calling {}, attempt {}".format(func, attempt))
            return await func(*args, **kwargs)
        except retry_exceptions:
            attempt += 1
            if attempt > attempts:
                log.warning("retry_async: {}: too many retries!".format(func))
                raise
            log.debug("retry_async: {}: sleeping before retry".format(func))
            await asyncio.sleep(sleeptime_callback(attempt))


def create_temp_creds(client_id, access_token, start=None, expires=None,
                      scopes=None, name=None):
    """Create temp TC creds from our permanent creds.
    """
    now = arrow.utcnow().replace(minutes=-10)
    start = start or now.datetime
    expires = expires or now.replace(days=31).datetime
    scopes = scopes or ['assume:project:taskcluster:worker-test-scopes', ]
    creds = createTemporaryCredentials(client_id, access_token, start, expires,
                                       scopes, name=name)
    for key, value in creds.items():
        try:
            creds[key] = value.decode('utf-8')
        except (AttributeError, UnicodeDecodeError):
            pass
    return creds


async def raise_future_exceptions(tasks):
    """Given a list of futures, await them, then raise their exceptions if
    any.  Without something like this, any exceptions will be ignored.
    """
    if not tasks:
        return
    await asyncio.wait(tasks)
    for task in tasks:
        exc = task.exception()
        if exc is not None:
            raise exc


def filepaths_in_dir(path):
    """Given a directory path, find all files in that directory, and return
    the relative paths to those files.
    """
    filepaths = []
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            filepath = filepath.replace(path, '').lstrip('/')
            filepaths.append(filepath)
    return filepaths


def get_hash(path, hash_type="sha256"):
    # I'd love to make this async, but evidently file i/o is always ready
    h = hashlib.new(hash_type)
    with open(path, "rb") as f:
        for chunk in iter(functools.partial(f.read, 4096), b''):
            h.update(chunk)
    return h.hexdigest()


def format_json(data):
    return json.dumps(data, indent=2, sort_keys=True)
