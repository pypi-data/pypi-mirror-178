# pylint: disable=missing-module-docstring

from datetime import datetime as dt
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from json import JSONEncoder

from ..entity.fields import FirestoreRef


def common_enc(obj: object):
    '''
    '''

    if isinstance(obj, dt):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, (IPv4Address, IPv6Address)):
        return obj.compressed

    return None


class StringEncoder(JSONEncoder):
    '''
    '''

    def default(self, o):

        if common_enc(o):
            return common_enc(o)
        elif isinstance(o, FirestoreRef):
            return str(o)

        return JSONEncoder.default(self, o)
