
# Dynamof

![Travis (.org](https://img.shields.io/travis/rayepps/dynamof)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e8c1e3cf175c007a591a/test_coverage)](https://codeclimate.com/github/rayepps/dynamof/test_coverage)
![PyPI - License](https://img.shields.io/pypi/l/dynamof)

A small :fire: interface for more easily making calls to dynamo using boto. No bloated ORM - just functions that make creating the complex objects needed to pass to boto3 quick and easy.

## Basic Features

- Simplifying `boto3` function APIs ([see an example](#example-create-a-table-in-dynamo))
> If you've ever used boto3 directly before you know the pain that can exist trying to write a generic `KeyCondition` or `ConditionExpression`. `dynamof` does these things for you. It provides simple functions that take common sense arguments and build the complex objects boto3 uses for you.

- Standardizing `boto3` error handling ([see an example](#example-catch-errors-from-dynamof))
> If you've ever used boto3 directly you know that handling errors is the absolute worst... how much time I've spent googling how to catch this error or that error.... and they're all different! `dynamof` wraps the calls to boto3, catches all of its errors, inspects them to determine the specific error it represents, and then throws a concrete and documented exception you can catch with a standard `try...except`.

- Its just a library
> `dynamof` is not a framework and its not opinionated. `dynamof` is simply a collection of deterministic functions that take in arguments and output boto3 command objects. We also provide a small wrapper for executing those boto3 calls behind the scenes if thats not something you want to do yourself. The benefit, is that you can use raw boto3 calls and `dynamof` calls right next to each other. `dyanmof` doesn't replace boto3, its a simple layer that sits on top to make things easier and more maintainable for you.

`dynamof` wraps the `boto3.client('dynamodb')` ([docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#dynamodb)) functions exposing much easier to use api's. It's written in a functional style with the goal to be as useful to anyone in any way as possible. The wrappers around boto3 functions are split into two parts: `operations` and `runners`. A runner runs a specific operations. The operation contains all the necessary information for a dynamo action to be ran. This means, you don't have to use `dynamof` to actually interact with dynamo if you don't want to but you could still use it as a utility to more easily generate the complex objects that are passed to boto3 functions.

## Why Dynamof?
If you're using python and dynamo you have 2 options: an ORM like PynamoDB or Boto3. Kudos to the people who made Pynamo, its great, but it really doesn't scale well. And your stuck with the ORM features even if you don't want them. Interacting with Boto3 directly is a pain. With things like `KeyCondition`s and `ConditionExpression`s being so difficult to easily grasp you end up duplicating a lot of code in your database/repository/DAL layer. This was my experience. In my early day's I used Pynamo. Once I got tired of trying to bend it to my will at scale I started using Boto3 directly. But... this was still annoying. I wanted a non-opinonated library that could sit on top of Botot3 and do the repetitive, annoying to code work for me. `dynamof` was born.

# Whats Supported?
See the two lists below for what has been implemented and what hasn't. If your a developer and want to do something thats not done yet its super easy to implement a new operation. See [the developer guide](#developer_guide) for directions.

## Currently Supported Calls

- :white_check_mark: Create table [[code](dynamof/operations/create.py) | [docs](#create_table) | [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table)]
- :white_check_mark: Describe table [[code](dynamof/operations/describe.py) | [docs](#describe_table) | [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_table)]
- :white_check_mark: Add item [[code](dynamof/operations/add.py) | [docs](#add_item) | [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item)]
- :white_check_mark: Find item [[code](dynamof/operations/find.py) | [docs](#find_item) | [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item)]
- :white_check_mark: Update item [[code](dynamof/operations/update.py) | [docs](#update_item) | [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item)]
- :white_check_mark: Delete item [[code](dynamof/operations/delete.py) | [docs](#delete_item) | [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_item)]
- :white_check_mark: Query table [[code](dynamof/operations/query.py) | [docs](#query_table) | [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query)]
- :white_check_mark: Scan table [[code](dynamof/operations/scan.py) | [docs](#scan_table) | [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan)]

## Currently Unsupported Calls
- :x: `batch_get_item` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.batch_get_item)]
- :x: `batch_write_item` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.batch_write_item)]
- :x: `can_paginate` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.can_paginate)]
- :x: `create_backup` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_backup)]
- :x: `create_global_table` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_global_table)]
- :x: `delete_backup` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_backup)]
- :x: `delete_table` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_table)]
- :x: `describe_backup` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_backup)]
- :x: `describe_continuous_backups` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_continuous_backups)]
- :x: `describe_contributor_insights` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_contributor_insights)]
- :x: `describe_endpoints` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_endpoints)]
- :x: `describe_global_table` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_global_table)]
- :x: `describe_global_table_settings` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_global_table_settings)]
- :x: `describe_limits` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_limits)]
- :x: `describe_table_replica_auto_scaling` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_table_replica_auto_scaling)]
- :x: `describe_time_to_live` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_time_to_live)]
- :x: `generate_presigned_url` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.generate_presigned_url)]
- :x: `get_paginator` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_paginator)]
- :x: `get_waiter` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_waiter)]
- :x: `list_backups` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_backups)]
- :x: `list_contributor_insights` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_contributor_insights)]
- :x: `list_global_tables` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_global_tables)]
- :x: `list_tables` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_tables)]
- :x: `list_tags_of_resource` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_tags_of_resource)]
- :x: `restore_table_from_backup` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.restore_table_from_backup)]
- :x: `restore_table_to_point_in_time` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.restore_table_to_point_in_time)]
- :x: `tag_resource` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.tag_resource)]
- :x: `transact_get_items` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.transact_get_items)]
- :x: `transact_write_items` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.transact_write_items)]
- :x: `untag_resource` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.untag_resource)]
- :x: `update_continuous_backups` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_continuous_backups)]
- :x: `update_contributor_insights` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_contributor_insights)]
- :x: `update_global_table` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_global_table)]
- :x: `update_global_table_settings` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_global_table_settings)]
- :x: `update_table` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_table)]
- :x: `update_table_replica_auto_scaling` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_table_replica_auto_scaling)]
- :x: `update_time_to_live` [[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_time_to_live)]


# Getting Started

## Example: Create a table in dynamo
```py
from boto3 import client
from dynamof.executor import execute
from dynamof.operations import create

client = client('dynamodb', endpoint_url='http://localstack:4569')

execute(client, create(table_name='users', hash_key='username'))
```
First thing to note... `execute(client, some_operation(...))` isn't _sexy_... and as engineers _sexy_ is important. Because `dynamof` is a simple functional utility library its very easy to bend it into any api you would like.

## Example: Customize the way you call dynamof
### Keep it functional
```py
from functools import partial
from boto3 import client
from dynamof.executor import execute
from dynamof.operations import create
from dynamof.attribute import attr

client = client('dynamodb', endpoint_url='http://localstack:4569')
db = partial(execute, client)

# Now calling looks like
db(create(table_name='users', hash_key='username'))
db(find(table_name='users', key={ 'username': 'sunshie '}))
db(update(
  table_name='users',
  key={ 'username': 'sunshie' },
  attributes={
      'roles': attr.append('admin'),
      'friends': attr.prepend('jake')
  }))
```

### Make it a class
```py
class DB:
  def __init__(self):
    self.client = client('dynamodb', endpoint_url='http://localstack:4569')
  def find(*args, **kwargs):
    return execute(self.client, find(*args, **kwargs))

db = DB()
db.find(table_name='users', key={ 'id': 21 })
```

### Make it a table specific class
```py
class Table:
  def __init__(self, table_name):
    client = client('dynamodb', endpoint_url='http://localstack:4569')
    self.table_name = table_name
    self.db = partial(execute, client)
  def find(*args, **kwargs):
    return self.db(find(self.table_name, *args, **kwargs))
  def update(*args, **kwargs):
    return self.db(update(self.table_name, *args, **kwargs))
  def delete(*args, **kwargs):
    return self.db(delete(self.table_name, *args, **kwargs))


users = Table('users')

users.find(key={ 'id': 21 })
users.update(key={ 'id': 21 }, attributes={ 'username': 'new_username_1993_bro' })
users.delete(key={'id': 21 })

```

## Example: Catch errors from dynamof
```py
from dynamof.exceptions import (
    UnknownDatabaseException,
    ConditionNotMetException,
    BadGatewayException,
    TableDoesNotExistException
)

try:
  db(update(
    table_name='users',
    key={ 'id': 43 },
    attributes={ 'username': 'sunshie' }))
except TableDoesNotExistException:
  # Handle case where table doesn't exist
except ConditionNotMetException:
  # Handle case where the condition wasn't met (the item you tried to update didn't exist)
except BadGatewayException:
  # Handle a network error
except UnknownDatabaseException:
  # Handle an unknown issue
```

## Example: Use dynamof to build boto3 arguments but still call boto3 yourself
```py
from dynamof import operations
from dynamof.conditions import attr


query = operations.query(
  table_name='books',
  conditions=attr('title').equals('The Cost of Discipleship'))

result = client.query(**query.description)
```

# API Documentation
[dynamof.operations](#operations)  
[dynamof.conditions](#conditions)  

## Operations
[See the code](dynamof/operations)
[See the test](test/unit/operations_test.py)  

### Create Table
```py
create(table_name, hash_key, allow_existing=False)
```

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name to assign the table your creating | `'users'` |
| `hash_key` | yes | `str` | The hash key (primary key) for your table | `'user_id'` |
| `allow_existing` | no | `bool` | Creating a table that already exists will throw an error in boto3. Passing `True` here will ignore that error if its raised and ignore it. | `True` |

#### :orange_book: Limitations
- Cannot specify range key
- Cannot specify complex hash key (hash key and range key)
- Cannot specify indexes
- Other boto3 parameters not implemented (`BillingMode`, `ProvisionedThroughput`, `StreamSpecification`, `SSESpecification`, `Tags`)

### Find Item
```py
find(table_name, key)
```

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to find an item in | `'users'` |
| `key` | yes | `str`\|`dict` | The key (primary key) of the item to find. If a string is passed it is associated with `id` by default. If an object is passed the first key and value are used to find the item | `22` or ```{ 'username': 'sunshie' }``` |

#### :orange_book: Limitations
- Cannot use projection expressions
- Other boto3 parameters not implemented (`ConsistentRead`, `ReturnConsumedCapacity`)


### Add Item
```py
add(table_name, item, auto_inc=False)
```

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to add the item to | `'users'` |
| `item` | yes | `dict` | The item to be added to the table in key value pairs. If `auto_inc` is not set to true then this dict **must** include a valid key value pair for the table's hash key | ```{ 'username': 'sunshie', 'user_status': 'unleashed' }``` |

#### :orange_book: Limitations
- boto3 parameters not implemented: `ReturnItemCollectionMetrics`, `ReturnConsumedCapacity`, `ReturnValues`

#### :closed_book: Known Issues
- When the table you're trying to add to does not exist the `put_item` function in boto3 does not throw the expected `ClientError` with the table not found code and message. Instead, it throws a bad gateway error. So, when calling `add` you cannot depend on the `TableDoesNotExistException`. In a future version you will be able to use an additonal method to check if the table exists if needed.


### Update Item
```py
update(table_name, key, attributes)
```

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to update the item on | `'users'` |
| `key` | yes | `str`\|`dict` | The key (primary key) of the item to find for updating. If a string is passed it is associated with `id` by default. If an object is passed the first key and value are used to find the item | `22` or ```{ 'username': 'sunshie' }``` |
| `attributes` | yes | `dict` | The key values patch/set on the record | ```{ 'rank': 23 }``` |

#### :orange_book: Limitations
- Cannot allow setting parameters for `ReturnValues`, `ReturnConsumedCapacity`, `ReturnItemCollectionMetrics`


### Delete Item
```py
delete(table_name, key)
```

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to delete the item from | `'users'` |
| `key` | yes | `str`\|`dict` | The key (primary key) of the item to delete. If a string is passed it is associated with `id` by default. If an object is passed the first key and value are used to find the item | `22` or ```{ 'username': 'sunshie' }``` |

#### :orange_book: Limitations
- Cannot allow setting parameters for `ReturnValues`, `ReturnConsumedCapacity`, `ReturnItemCollectionMetrics`


### Query Table
```py
query(table_name, conditions)
```

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to execute the query on | `'users'` |
| `conditions ` | yes | `dynamof.conditions.Condition` | This value should be built using the `dynamof.conditions` module. See the docs on that module. | `attr('username').equals('sunshie')` will build a proper Condition to pass. |

#### :orange_book: Limitations
- Cannot do pagination
- Cannot set limits
- Cannot query indexes
- Cannot allow setting parameters for `ReturnValues`, `ReturnConsumedCapacity`, `ReturnItemCollectionMetrics`


## Conditions

The `dynamof.conditions` module provides utility methods that make it simple to generate the complex data object boto3 needs when specifying conditions for querying, scanning, and other operations. Looking at the [docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query) for the query function you'll see `KeyConditionExpression`. This is the parameter this module was created to build.

**Example**

```py
from dynamof.conditions import attr

cond = attr('username').equals('sunshie')

cond.expression
# 'username = :username'

cond.attr_values
# { ":username": { "S": "sunshie" } }

```



### attr(name)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `name`  | yes  | `str` | The name of the attribute to begin using on a condition. Could be a column you want to match exactly or if its a number type then it could be a column you want to check for `>` or `<` on | `'username'` |


The `attr` function returns a `dynamof.conditions.Attribute` that contains three methods

* `equals(value)`
* `greater_than(value)`
* `less_than(value)`

Where value is always the value to use in the conditional comparison you build.

### cand(\*conditions)

Takes any number of condition expressions and combines them using the _and_ rule.

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `conditions`  | yes  | `*dynamof.conditions.Condition` | Takes any number of `Condition` instances  | `cand(attr('points').less_than(50)` |

# Developer Guide
As a developer you can probably guide yourself, you just want to know in simple terms "how it works". Thats what I'll talk about here - the design, what calls what, what does what. After reading the developer guide you should feel comfortable making changes.

## The Design
The goal when `dynamof` was started was to create the complicated objects that boto3 takes in as arguments to its calls. It wasn't until later that a wrapper for executing those calls inside `dynamof` was added so we could standardize wild boto3 exceptions for the client. This means, at the core of `dynamof` is `operations` and `builder` - its that simple. The builder is (for the most part) a DTO (with some sugar) for containg all the arguments you specify for a given operation. If you look in any operation file you'll find the same pattern:
```py
def operation_name(table_name, key, conditions=None):

    # Build is a function we can use to create boto3 arguments with the details
    # we pass to `ab.builder`. For example, `build(ab.TableName)` will return the
    # `table_name` we pass the builder here.
    build = ab.builder(
        table_name=table_name,
        key=key,
        conditions=conditions)

    # Description is the object that will get passed to the boto3 call. See `run` below.
    description = shake(
        TableName=build(ab.TableName),
        Key=build(ab.Key),
        ConditionExpression=build(ab.ConditionExpression),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues))

    return Operation(description, run)

def run(client, description):
    # This is where boto3 will be called - if so desired. In the executor this function gets wrapped
    # in error handling. Again, a pure function (ish - because were making a network call - but as
    # pure as pure can be for a network calling function).
    res = client.operation_name(**description)
    return response(res) # Returns a standard response object
```
You can see, this doesn't call dynamo or boto3, its a deterministic/pure function that takes in arguments and uses the builder to generate all the arguments for the boto3 call.

### How it effects tests
Since the operation functions return an `Operation` we can write concise, full coverage tests by calling the operation function with different arguments and then looking in on the `description` it returned in side the `Operation`. Heres an example:
```py
def test_operation_creates_description_with_table_name():
    res = operation_name(table_name='users', key={ 'username': 'sunshie '})
    assert res.description['TableName'] == 'users'
```

## How to add an operation
Given the information above, here is a checklist you might use when addding a new operation. For example sake, lets say the operation name is `deploy`.
1. Create a file for the new `deploy` operation at `dynamof/operations/deploy.py`
2. Define two functions inside this file `deploy(...)` and `run(client, description)`
3. Add any arguments you might need to the `deploy` function
4. Use the builder to generate all the arguments boto3 expects given the `deploy` function arguments.
5. If needed, go to the builder, and add/modify the functions that create description attributes.
6. Implement the `run` method. The executor expects all `run` functions to take a `client` and `description` and return a `response`. This should always be a stupid simple function that just calls boto3 and returns the result.
You have a new operation you can use!
