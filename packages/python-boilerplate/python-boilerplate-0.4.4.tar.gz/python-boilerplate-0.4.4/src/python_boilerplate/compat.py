from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
import six
from unidecode import unidecode as _unidecode


if six.PY2:
    _unicode = unicode

    def unidecode(x):
        if not isinstance(x, _unicode):
            x = six.u(x)
        return _unidecode(x)

    def unicode(x):
        if isinstance(x, str):
            return x.decode('utf8')
        return _unicode(x)

else:
    unidecode = _unidecode

    def unicode(x):
        if isinstance(x, bytes):
            return x.decode('utf8')
        return str(x)
