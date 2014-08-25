__author__ = 'roy'

import multiprocessing
import codecs

from nose.plugins.base import Plugin
from nose.plugins.xunit import Xunit
from nose.pyversion import force_unicode
from nose_htmloutput import HtmlOutput


MANAGER = multiprocessing.Manager()
MP_ERRORLIST = MANAGER.list()
MP_STATS = MANAGER.dict()

class HtmlMp(object):
    pass