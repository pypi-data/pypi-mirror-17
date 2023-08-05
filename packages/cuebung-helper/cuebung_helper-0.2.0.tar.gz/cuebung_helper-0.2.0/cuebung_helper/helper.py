"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        helper.py -- helper functions for testing c funktions

    FIRST RELEASE
        2016-06-29  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
import abc
from collections import namedtuple
from cuebung_helper import __version__

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"

Command = namedtuple('Command', ['ldpreload', 'filename'])
Config = namedtuple('Config', ['use_stdin', 'command', 'args'])


def _islistofstrings(arg):
    """Check if `arg` is a list of strings or an empty list"""
    ret = False
    if isinstance(arg, list):
        ret = all(isinstance(entry, str) for entry in arg)
    return ret


def _cmplistofstrings(list_a, list_b):
    """Compare two list of strings for equaltity"""
    if len(list_a) != len(list_b):
        return False
    if not all(str_a == str_b for str_a, str_b in zip(list_a, list_b)):
        return False
    return True


def _cleanresult(result, encoding='utf-8', errors='replace', strip='\n'):
    """Convert the stdout/stderr from popen in a list of strings"""
    return _lob2los(result.readlines(), encoding, errors, strip)


def _lob2los(listofbytes, encoding='utf-8', errors='replace', strip='\n'):
    """Convert a list of bytestrings in a list of strings"""
    output = []
    for line in listofbytes:
        sline = line.decode(encoding, errors=errors).strip(strip)
        if len(sline) > 0:
            output.append(sline)
    return output


class AutoStorage:
    """Base Descriptor"""
    __counter = 0
    _default = None

    def __init__(self, value=None):
        self.other_value = value
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter  # pylint: disable=W0212
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:  # pragma: no cover
            return self  # pragma: no cover
        else:
            return getattr(instance, self.storage_name, self.other_value)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    """Descriptor class with abstract validator"""

    def __init__(self, value=None):
        value = self.validate(None, value)
        super().__init__(value)
        self.other_value = value or self._default

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise an ValueError"""


class Boolean(Validated):
    """Boolean Validator"""
    _default = False

    def validate(self, instance, value):
        """return validated value or raise an ValueError"""
        if isinstance(value, bool) or (instance is None and value is None):
            return value
        else:
            raise ValueError('value must be a bool')


class Text(Validated):
    """Text Validator"""

    def validate(self, instance, value):
        """return validated value or raise an ValueError"""
        if isinstance(value, str) or (instance is None and value is None):
            return value
        else:
            raise ValueError('value must be a string')
# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
