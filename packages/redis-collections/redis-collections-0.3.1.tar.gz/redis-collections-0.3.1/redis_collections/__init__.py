# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__title__ = 'redis-collections'
__version__ = '0.3.1'
__author__ = 'Honza Javorek'
__license__ = 'ISC'
__copyright__ = 'Copyright 2013-? Honza Javorek'


from .base import RedisCollection  # NOQA
from .dicts import DefaultDict, Dict, Counter  # NOQA
from .lists import Deque, List  # NOQA
from .sets import Set  # NOQA

__all__ = [
    'Counter',
    'DefaultDict',
    'Deque',
    'Dict',
    'List',
    'RedisCollection',
    'Set',
]
