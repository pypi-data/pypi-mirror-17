"""Feed Errors.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ElementNotFound(Exception):
    pass


class ElementRequired(Exception):
    pass


class UnsupportedElement(Exception):
    pass


class ReadError(Exception):
    pass
