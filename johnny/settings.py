from django.conf import settings

DISABLE_QUERYSET_CACHE = getattr(settings, 'DISABLE_QUERYSET_CACHE', False)

BLACKLIST = getattr(settings, 'MAN_IN_BLACKLIST',
            getattr(settings, 'JOHNNY_TABLE_BLACKLIST', []))
BLACKLIST = set(BLACKLIST)

MIDDLEWARE_KEY_PREFIX = getattr(settings, 'JOHNNY_MIDDLEWARE_KEY_PREFIX', 'jc')

MIDDLEWARE_SECONDS = getattr(settings, 'JOHNNY_MIDDLEWARE_SECONDS', 0)

CACHE_BACKEND = getattr(settings, 'JOHNNY_CACHE_BACKEND',
                getattr(settings, 'CACHE_BACKEND', None))

CACHES = getattr(settings, 'CACHES', {})

DATABASE_MAPPING = getattr(settings, "JOHNNY_DATABASE_MAPPING", {})

def _get_backend():
    """Returns the actual django cache object johnny is configured to use.
    This relies on the settings only;  the actual active cache can
    theoretically be changed at runtime."""
    from django.core.cache import get_cache, cache
    enabled = [n for n,c in sorted(CACHES.items()) if c.get('JOHNNY_CACHE', False)]
    if len(enabled) > 1:
        from warnings import warn
        warn("Multiple caches configured for johnny-cache; using %s." % enabled[0])
    if enabled:
        return get_cache(enabled[0])
    if CACHE_BACKEND:
        backend = get_cache(CACHE_BACKEND)
        if backend not in CACHES:
            from django.core import signals
            # Some caches -- python-memcached in particular -- need to do a cleanup at the
            # end of a request cycle. If the cache provides a close() method, wire it up
            # here.
            if hasattr(backend, 'close'):
                signals.request_finished.connect(backend.close)
        return backend
    return cache

