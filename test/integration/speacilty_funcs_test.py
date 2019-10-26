import json
import pytest
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynamof import funcs
from dynamof.conditions import attr
from dynamof.operations import (
    create,
    find,
    add,
    update,
    delete,
    query
)

def test_update_list_by_append(db):

    db(create(
        table_name='funcs',
        hash_key='id',
        allow_existing=True))

    db(add(table_name='funcs', item={
        'id': 'aaa',
        'items': [ 'a', 'b', 'c' ]
    }))

    db(update(table_name='funcs', key={'id': 'aaa'}, attributes={
        'items': funcs.append('D')
    }))

    record = db(find(table_name='funcs', key={
        'id': 'aaa'
    }))

    items = record.get('item').get('items')

    assert isinstance(items, list)
    assert 'D' in items
