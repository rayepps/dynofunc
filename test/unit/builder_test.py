import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from dynamof import builder as ab

def test_update_expression():
    res = ab.update_expression({
        'owner': 'ray',
        'status': 'ON'
    })
    assert res == 'SET owner = :owner, status = :status'

def test_expression_attribute_values():
    res = ab.expression_attribute_values({
        'owner': 'ray',
        'status': 'ON'
    })
    assert res[':owner']['S'] == 'ray'
    assert res[':status']['S'] == 'ON'

def test_condition_expression_uses_primitive():
    res = ab.condition_expression('abcd13')
    assert res == 'id = :id'

def test_condition_expression_uses_obj():
    res = ab.condition_expression({
        'myid': 'abcd13'
    })
    assert res == 'myid = :myid'

def test_value_type_tree():

    class BadValue:
        pass

    res = ab.value_type_tree({
        'username': 'rayepps',
        'user_id': 23,
        'roles': set([ 'admin', 'user' ]),
        'friend_ids': set([ 23, 282, 98 ]),
        'timming': [ 23, 56, 22, 11 ],
        'position': None,
        'isActive': True,
        'extra': {
            'food': [ 'american', 43 ]
        },
        'danger': 'τoρνoς'.encode('utf-8'),
        'danger_set': set([ 'τoρνoς'.encode('utf-8') ]),
        'mixed_danger_set': set([ 'τoρνoς'.encode('utf-8'), 'x', 23 ]),
        'klass': BadValue()
    })

    # Assert string type is built
    assert res['username'] is not None
    assert res['username']['S'] == 'rayepps'

    # Assert number type is built
    assert res['user_id'] is not None
    assert res['user_id']['N'] == 23

    # Assert byte type is built
    assert res['danger'] is not None
    assert res['danger']['B'] == 'τoρνoς'.encode('utf-8')

    # Assert bool type is built
    assert res['isActive'] is not None
    assert res['isActive']['BOOL'] == True

    # Assert string set type is built
    assert res['roles'] is not None
    assert 'user' in res['roles']['SS']
    assert 'admin' in res['roles']['SS']

    # Assert string set type is built
    assert res['friend_ids'] is not None
    assert 23 in res['friend_ids']['NS']
    assert 98 in res['friend_ids']['NS']

    # Assert list type is built
    assert res['timming'] is not None
    assert res['timming']['L'] is not None
    assert res['timming']['L'][0]['N'] == 23
    assert res['timming']['L'][1]['N'] == 56
    assert res['timming']['L'][2]['N'] == 22

    # Assert null type is built
    assert res['position'] is not None
    assert res['position']['NULL'] is True

    # Assert dict type is built
    assert res['extra'] is not None
    assert res['extra']['M'] is not None
    assert res['extra']['M']['food']['L'][0]['S'] == 'american'
    assert res['extra']['M']['food']['L'][1]['N'] == 43

    # Assert set(byte) type is built
    assert res['danger_set'] is not None
    assert 'τoρνoς'.encode('utf-8') in res['danger_set']['BS']

    # Assert set(byte) type is built
    assert res['mixed_danger_set'] is not None
    assert 23 in res['mixed_danger_set']['SS']
    assert 'x' in res['mixed_danger_set']['SS']

    # Assert unknown type (class) gets defaulted to string
    assert res['klass'] is not None
    assert res['klass']['S'] is not None

def test_destructure_type_tree():
    res = ab.destructure_type_tree({
        "id": {
            "S": "aaa"
        },
        "username": {
            "S": "sunshie"
        }
    })
    assert res['id'] == 'aaa'
    assert res['username'] == 'sunshie'