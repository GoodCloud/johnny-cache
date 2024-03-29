#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Threadlocal OpenStruct-like cache."""

import re
import fnmatch
import threading

class LocalStore(threading.local):
    """A thread-local OpenStruct that can be used as a local cache.  An instance
    is located at ``johnny.cache.local``, and is cleared on every request by the
    ``LocalStoreClearMiddleware``.  It can be a thread-safe way to handle global
    contexts."""
    def __init__(self, **d):
        threading.local.__init__(self)
        for k,v in d.iteritems():
            threading.local.__setattr__(self, k, v)
    # dictionary API
    def __getitem__(self, key):
        return self.__dict__[key]
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    def __delitem__(self, key):
        if key in self.__dict__:
            del self.__dict__[key]
    def __iter__(self):
        return iter(self.__dict__)
    def __len__(self): return len(self.__dict__)
    def keys(self): return self.__dict__.keys()
    def values(self): return self.__dict__.values()
    def items(self): return self.__dict__.items()
    def iterkeys(self): return self.__dict__.iterkeys()
    def itervalues(self): return self.__dict__.itervalues()
    def iteritems(self): return self.__dict__.iteritems()
    def get(self, *args): return self.__dict__.get(*args)
    def update(self, d): self.__dict__.update(d)
    def setdefault(self, name, value): return self.__dict__.setdefault(name, value)
    def mget(self, pat=None):
        """Get a dictionary mapping of all k:v pairs with key matching
        glob style expression `pat`."""
        if pat is None: return {}
        expr = re.compile(fnmatch.translate(pat))
        m = {}
        for key in self.keys():
            #make sure the key is a str first
            if type(key) in (str, unicode):
                if expr.match(key):
                    m[key] = self[key]
        return m

    def clear(self, pat=None):
        """Minor diversion with built-in dict here;  clear can take a glob
        style expression and remove keys based on that expression."""
        if pat is None:
            return self.__dict__.clear()
        expr = re.compile(fnmatch.translate(pat))
        for key in self.keys():
            #make sure the key is a str first
            if type(key) in (str, unicode):
                if expr.match(key):
                    del self.__dict__[key]

    def __repr__(self): return repr(self.__dict__)
    def __str__(self): return str(self.__dict__)

