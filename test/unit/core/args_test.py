import pytest
import json
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.assertions import assertObjectsEqual

from dynamof.core import args
from dynamof.core.utils import immutable

def test_GlobalSecondaryIndexes_result():
    mock_request = immutable(
        gsi=[dict(
            name='gs_index',
            hash_key='other',
            range_key='type'
        )])

    expected = [{
        'IndexName': 'gs_index',
        'KeySchema': [
            {
                'AttributeName': 'other',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'type',
                'KeyType': 'RANGE'
            }
        ],
        'Projection': {
            'ProjectionType': 'ALL'
        },
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }]

    result = args.GlobalSecondaryIndexes(mock_request)

    assertObjectsEqual(result, expected)

def test_LocalSecondaryIndexes_result():
    mock_request = immutable(
        hash_key='main_hash_key',
        lsi=[dict(
            name='gs_index',
            range_key='type'
        )])

    expected = [{
        'IndexName': 'gs_index',
        'KeySchema': [
            {
                'AttributeName': 'main_hash_key',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'type',
                'KeyType': 'RANGE'
            }
        ],
        'Projection': {
            'ProjectionType': 'ALL'
        }
    }]

    result = args.LocalSecondaryIndexes(mock_request)

    assertObjectsEqual(result, expected)

def test_AttributeDefinitions_gets_all_keys():
    mock_request = immutable(
        hash_key='id',
        range_key='country',
        lsi=[dict(
            name='gs_index',
            range_key='type'
        )],
        gsi=[dict(
            name='gs_index',
            hash_key='username',
            range_key='status'
        )])

    expected = [ 'id', 'type', 'username', 'status', 'country' ]

    result = [item.get('AttributeName') for item in args.AttributeDefinitions(mock_request)]

    assert set(expected) == set(result)

def test_AttributeDefinitions_does_not_duplicate_keys():
    mock_request = immutable(
        hash_key='id',
        range_key='country',
        lsi=[dict(
            name='gs_index',
            range_key='type'
        )],
        gsi=[dict(
            name='gs_index',
            hash_key='country',
            range_key='status'
        )])

    result = [item.get('AttributeName') for item in args.AttributeDefinitions(mock_request)]

    assert len([1 for key in result if key == 'country']) == 1

def test_KeySchema_uses_hash_and_range():
    mock_request = immutable(
        hash_key='id',
        range_key='type')

    expected = [
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'type',
            'KeyType': 'RANGE'
        }
    ]

    result = args.KeySchema(mock_request)

    assertObjectsEqual(result, expected)
