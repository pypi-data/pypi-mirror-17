import logging
import functools
import contextlib


logger = logging.getLogger(__name__)
_CACHE = {}


class CacheOptions(object):
    def __init__(self):
        self.enabled = True
        self.debug = False


options = CacheOptions()


def _set_log_lvl():
    """ Make sure that logging is respecting the debug setting """
    logger.setLevel(logging.DEBUG if options.debug else logging.INFO)


def has(key):
    """ See if a key is in the cache

    >>> from minicache import cache
    >>> cache.has('has?')
    False
    >>> cache.update('has?', 'now')
    >>> cache.has('has?')
    True
    """
    _set_log_lvl()
    logger.debug('has %s', key)
    return key in _CACHE.keys() and options.enabled


def update(key, value):
    """ Perform update key value on the cache

    >>> from minicache import cache
    >>> cache.get('update!')
    >>> cache.update('update!', 'this')
    >>> cache.get('update!')
    'this'
    >>> cache.update('update!', 'that')
    >>> cache.get('update!')
    'that'
    """
    _set_log_lvl()
    logger.debug('update %s, %s', key, value)
    if not options.enabled:
        return
    _CACHE[key] = value


def get(key, default=None):
    """ Get a value out of the cache, return default if key not found
    or cache is disabled

    >>> from minicache import cache
    >>> cache.get('get!')
    >>> cache.get('get!', 'default')
    'default'
    >>> cache.update('get!', 'got')
    >>> cache.get('get!', 'default')
    'got'
    """
    _set_log_lvl()
    logger.debug('get %s, default=%s', key, default)
    if has(key):
        return _CACHE[key]
    return default


def clear(key=None):
    """ Clear a cache entry, or the entire cache if no key is given

    >>> from minicache import cache
    >>> cache.update('clear!', 'now')
    >>> cache.update("don't!", 'yet')
    >>> cache.has('clear!')
    True
    >>> cache.has("don't!")
    True
    >>> cache.clear('clear!')
    >>> cache.has('clear!')
    False
    >>> cache.has("don't!")
    True
    >>> cache.clear()
    >>> cache.has("don't!")
    False
    """
    _set_log_lvl()
    logger.debug('clear %s', key)
    if not options.enabled:
        return
    elif key is not None and key in _CACHE.keys():
        del _CACHE[key]
    elif not key:
        for cached_key in [k for k in _CACHE.keys()]:
            del _CACHE[cached_key]


def this(func):
    """ Use the cache as a decorator, essentially this with an override

    >>> from minicache import cache
    >>> @cache.this
    ... def dummy():
    ...     print('in the func')
    ...     return 'value'
    ...
    >>> dummy()
    in the func
    'value'
    >>> dummy()
    'value'
    """

    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        _set_log_lvl()
        key = func.__name__ + str(args) + str(kwargs)
        logger.debug('this %s' ,key)

        if has(key) and options.enabled:
            return get(key)

        value = func(*args, **kwargs)

        if options.enabled:
            update(key, value)

        return value

    return func_wrapper


def disable(clear_cache=True):
    """ Disable the cache and clear its contents

    >>> from minicache import cache
    >>> cache.update('disable!', 'me')
    >>> cache.disable()
    >>> cache.has('disable!')
    False
    >>> cache.enable()
    >>> cache.has('disable!')
    False
    """
    _set_log_lvl()
    logger.debug('disable clear_cache %s', clear_cache)

    if clear_cache:
        clear()

    options.enabled = False


def enable():
    """ (Re)enable the cache

    >>> from minicache import cache
    >>> cache.disable()
    >>> cache.update('enable!', 'or not')
    >>> cache.has('enable!')
    False
    >>> cache.enable()
    >>> cache.update('enable!', 'now')
    >>> cache.has('enable!')
    True
    """
    _set_log_lvl()
    logger.debug('enable!')

    options.enabled = True


@contextlib.contextmanager
def temporarily_disabled():
    """ Temporarily disable the cache

    >>> from minicache import cache
    >>> with cache.temporarily_disabled():
    ...     cache.update('temp', 'disable')
    ...
    >>> cache.has('temp')
    False
    """
    old_setting = options.enabled
    options.enabled = False
    yield
    options.enabled = old_setting


@contextlib.contextmanager
def temporarily_enabled():
    """ Temporarily enable the cache

    >>> from minicache import cache
    >>> with cache.temporarily_disabled():
    ...     with cache.temporarily_enabled():
    ...         cache.update('temp', 'disable')
    ...
    >>> cache.has('temp')
    True
    """
    old_setting = options.enabled
    options.enabled = True
    yield
    options.enabled = old_setting
