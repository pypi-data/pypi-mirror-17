VERSION = '0.2.2'
VERSION_STATUS = ''

_items = VERSION.split('-')
VERSION_NUMBER_PARTS = tuple(int(i) for i in _items[0].split('.'))
if len(_items) > 1:
    VERSION_STATUS = _items[1]
__version__ = VERSION
