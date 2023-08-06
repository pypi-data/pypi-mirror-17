"""
This module contains the high-level functions to access the library. Care is
taken to make this as pythonic as possible and hide as many of the gory
implementations as possible.
"""
from typing import List, Tuple

from .x690.types import (
    Integer,
    ObjectIdentifier,
    OctetString,
    Sequence,
    Type,
)
from .x690.util import tablify
from .exc import SnmpError
from .pdu import (
    GetNextRequest,
    GetRequest,
    SetRequest,
    VarBind,
)
from .const import Version
from .transport import send, get_request_id


def get(ip: str, community: str, oid: str, port: int=161):
    """
    Executes a simple SNMP GET request and returns a pure Python data structure.

    Example::

        >>> get('192.168.1.1', 'private', '1.2.3.4')
        'non-functional example'
    """
    return multiget(ip, community, [oid], port)[0]


def multiget(ip: str, community: str, oids: List[str], port: int=161):
    """
    Executes an SNMP GET request with multiple OIDs and returns a list of pure
    Python objects. The order of the output items is the same order as the OIDs
    given as arguments.

    Example::

        >>> multiget('192.168.1.1', 'private', ['1.2.3.4', '1.2.3.5'])
        ['non-functional example', 'second value']
    """

    oids = [ObjectIdentifier.from_string(oid) for oid in oids]

    packet = Sequence(
        Integer(Version.V2C),
        OctetString(community),
        GetRequest(get_request_id(), *oids)
    )

    response = send(ip, port, bytes(packet))
    raw_response = Sequence.from_bytes(response)

    output = [value.pythonize() for _, value in raw_response[2].varbinds]
    if len(output) != len(oids):
        raise SnmpError('Unexpected response. Expected %d varbind, '
                        'but got %d!' % (len(oids), len(output)))
    return output


def getnext(ip, community, oid, port):
    """
    Executes a single SNMP GETNEXT request (used inside *walk*).

    Example::

        >>> getnext('192.168.1.1', 'private', '1.2.3')
        VarBind(ObjectIdentifier(1, 2, 3, 0), 'non-functional example')
    """
    return multigetnext(ip, community, [oid], port)[0]


def multigetnext(ip, community, oids, port=161):
    """
    Function to send a single multi-oid GETNEXT request.

    The request sends one packet to the remote host requesting the value of the
    OIDs following one or more given OIDs.

    Example::

        >>> multigetnext('192.168.1.1', 'private', ['1.2.3', '1.2.4'])
        [
            VarBind(ObjectIdentifier(1, 2, 3, 0), 'non-functional example'),
            VarBind(ObjectIdentifier(1, 2, 4, 0), 'second value')
        ]
    """
    request = GetNextRequest(get_request_id(), *oids)
    packet = Sequence(
        Integer(Version.V2C),
        OctetString(community),
        request
    )
    response = send(ip, port, bytes(packet))
    raw_response = Sequence.from_bytes(response)
    response_object = raw_response[2]
    if len(response_object.varbinds) != len(oids):
        raise SnmpError(
            'Invalid response! Expected exactly %d varbind, '
            'but got %d' % (len(oids), len(response_object.varbinds)))
    return response_object.varbinds


def walk(ip: str, community: str, oid, port: int=161):
    """
    Executes a sequence of SNMP GETNEXT requests and returns an generator over
    :py:class:`~puresnmp.pdu.VarBind` instances.

    The generator stops when hitting an OID which is *not* a sub-node of the
    given start OID or at the end of the tree (whichever comes first).

    Example::

        >>> walk('127.0.0.1', 'private', '1.3.6.1.2.1.1')
        <generator object multiwalk at 0x7fa2f775cf68>

        >>> from pprint import pprint
        >>> pprint(list(walk('127.0.0.1', 'private', '1.3.6.1.2.1.3')))
        [VarBind(oid=ObjectIdentifier((1, 3, 6, 1, 2, 1, 3, 1, 1, 1, 24, 1, 172, 17, 0, 1)), value=Integer(24)),
         VarBind(oid=ObjectIdentifier((1, 3, 6, 1, 2, 1, 3, 1, 1, 2, 24, 1, 172, 17, 0, 1)), value=OctetString(b'\\x02B\\xef\\x14@\\xf5')),
         VarBind(oid=ObjectIdentifier((1, 3, 6, 1, 2, 1, 3, 1, 1, 3, 24, 1, 172, 17, 0, 1)), value=NonASN1Type(64, b'\\xac\\x11\\x00\\x01'))]
    """

    return multiwalk(ip, community, [oid], port)


def multiwalk(ip: str, community: str, oids: List[str], port: int=161):
    """
    Executes a sequence of SNMP GETNEXT requests and returns an generator over
    :py:class:`~puresnmp.pdu.VarBind` instances.

    This is the same as :py:func:`~.walk` except that it is capable of iterating
    over multiple OIDs at the same time.

    Example::

        >>> walk('127.0.0.1', 'private', ['1.3.6.1.2.1.1', '1.3.6.1.4.1.1'])
        <generator object multiwalk at 0x7fa2f775cf68>

    """

    varbinds = multigetnext(ip, community, oids, port)

    retrieved_oids = [str(bind.oid) for bind in varbinds]
    prev_retrieved_oids = []
    while retrieved_oids:
        for bind in varbinds:
            yield bind

        varbinds = multigetnext(ip, community, retrieved_oids, port)
        retrieved_oids = [str(bind.oid) for bind in varbinds]

        # ending condition (check if we need to stop the walk)
        retrieved_oids_ = [ObjectIdentifier.from_string(_)
                           for _ in retrieved_oids]
        requested_oids = [ObjectIdentifier.from_string(_)
                          for _ in oids]
        contained_oids = [
            a in b for a, b in zip(retrieved_oids_, requested_oids)]
        if not all(contained_oids) or retrieved_oids == prev_retrieved_oids:
            return

        prev_retrieved_oids = retrieved_oids


def set(ip: str, community: str, oid: str, value: Type, port: int=161):
    """
    Executes a simple SNMP SET request. The result is returned as pure Python
    data structure. The value must be a subclass of
    :py:class:`~puresnmp.x690.types.Type`.

    Example::

        >>> set('127.0.0.1', 'private', '1.3.6.1.2.1.1.4.0',
        ...     OctetString(b'I am contact'))
        b'I am contact'
    """

    result = multiset(ip, community, [(oid, value)], port)
    return result[oid]


def multiset(ip: str, community: str, mappings: List[Tuple[str, Type]],
             port: int=161):
    """

    Executes an SNMP SET request on multiple OIDs. The result is returned as
    pure Python data structure.

    Fake Example::

        >>> multiset('127.0.0.1', 'private', [('1.2.3', OctetString(b'foo')),
        ...                                   ('2.3.4', OctetString(b'bar'))])
        {'1.2.3': b'foo', '2.3.4': b'bar'}
    """

    if any([not isinstance(v, Type) for k, v in mappings]):
        raise TypeError('SNMP requires typing information. The value for a '
                        '"set" request must be an instance of "Type"!')

    binds = [VarBind(ObjectIdentifier.from_string(k), v)
             for k, v in mappings]

    request = SetRequest(get_request_id(), binds)
    packet = Sequence(Integer(Version.V2C),
                      OctetString(community),
                      request)
    response = send(ip, port, bytes(packet))
    raw_response = Sequence.from_bytes(response)
    output = {
        str(oid): value.pythonize() for oid, value in raw_response[2].varbinds
    }
    if len(output) != len(mappings):
        raise SnmpError('Unexpected response. Expected %d varbinds, '
                        'but got %d!' % (len(mappings), len(output)))
    return output


def table(ip: str, community: str, oid: str, port: int=161,
          num_base_nodes: int=0):
    """
    Run a series of GETNEXT requests on an OID and construct a table from the
    result.

    The table is a row of dicts. The key of each dict is the row ID. By default
    that is the **last** node of the OID tree.

    If the rows are identified by multiple nodes, you need to secify the base by
    setting *walk* to a non-zero value.
    """
    tmp = walk(ip, community, oid, port=port)
    as_table = tablify(tmp, num_base_nodes=num_base_nodes)
    return as_table
