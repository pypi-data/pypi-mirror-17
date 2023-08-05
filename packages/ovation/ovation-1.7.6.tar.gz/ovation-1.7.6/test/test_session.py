import requests.exceptions
from nose.tools import istest, assert_equal
from six.moves.urllib_parse import urljoin
from unittest.mock import Mock, sentinel
import ovation.session as connection


@istest
def should_set_session_token():
    token = 'my-token'
    s = connection.Session(token)

    assert_equal(s.token, token)


@istest
def should_set_api_base():
    token = 'my-token'
    api_base = 'https://my.server/'
    s = connection.Session(token, api=api_base)

    path = '/api/v1/some/path'
    assert_equal(s.make_url(path), urljoin(api_base, path))

@istest
def should_add_prefix():
    token = 'my-token'
    api_base = 'https://my.server/'
    s = connection.Session(token, api=api_base)

    path = '/some/path'
    assert_equal(s.make_url(path), urljoin(api_base, '/api/v1' + path))


@istest
def should_make_type_index_url():
    s = connection.Session(sentinel.token)

    assert_equal(s.entity_path('project'), '/projects/')


@istest
def should_make_type_get_url():
    s = connection.Session(sentinel.token)

    assert_equal(s.entity_path('project', entity_id='123'), '/projects/123')


@istest
def should_return_single_entry_value():
    s = connection


    entities = ['foo', 'bar']
    assert_equal(s.simplify_response({'entities': entities}), entities)


@istest
def should_return_datadict():
    s = connection
    result = s.simplify_response({'bar': 'baz',
                                  'foo': sentinel.bar})

    assert_equal(result.bar, 'baz')


@istest
def should_return_multientry_keys_and_values():
    s = connection

    d = {'entities': sentinel.entities,
         'others': 'foo'}
    assert_equal(s.simplify_response(d), d)

@istest
def should_simplify_tags_response():
    s = connection
    d = {
        "tags": [
            {
                "_id": "b1a268af-3bf1-4a13-a530-68e9cc4b9367",
                "user": "5162ef4f-8c57-4c2c-8e35-2a3f4f114275",
                "entity": "f2bfa3da-7eae-45c4-80a5-9e9a3588a237",
                "annotation_type": "tags",
                "annotation": {
                    "tag": "mytag"
                },
                "type": "Annotation",
                "links": {
                    "_collaboration_roots": [
                        "f2bfa3da-7eae-45c4-80a5-9e9a3588a237"
                    ]
                },
                "permissions": {
                    "update": True,
                    "delete": True
                }
            }
        ]
    }

    expected = [
            {
                "_id": "b1a268af-3bf1-4a13-a530-68e9cc4b9367",
                "user": "5162ef4f-8c57-4c2c-8e35-2a3f4f114275",
                "entity": "f2bfa3da-7eae-45c4-80a5-9e9a3588a237",
                "annotation_type": "tags",
                "annotation": {
                    "tag": "mytag"
                },
                "type": "Annotation",
                "links": {
                    "_collaboration_roots": [
                        "f2bfa3da-7eae-45c4-80a5-9e9a3588a237"
                    ]
                },
                "permissions": {
                    "update": True,
                    "delete": True
                }
            }
        ]

    assert_equal(s.simplify_response(d), expected)


@istest
def should_clean_for_update():
    token = 'my-token'
    api_base = 'https://my.server/'
    path = '/api/v1/updates/1'

    response = Mock()
    response.raise_for_status = Mock(return_value=None)
    response.json = Mock(return_value=sentinel.resp)

    s = connection.Session(token, api=api_base)
    s.session.put = Mock(return_value=response)

    entity = {'_id': 1,
              'type': 'Entity',
              'attributes': {'foo': 'bar'},
              'links': {'self': 'url'},
              'owner': 1,
              'relationships': {}}
    expected = {'_id': 1,
                'type': 'Entity',
                'attributes': {'foo': 'bar'}}

    r = s.put(path, entity=entity)
    assert_equal(r, sentinel.resp)
    s.session.put.assert_called_with(urljoin(api_base, path),
                                     json={'entity': expected})

@istest
def should_proxy_get_requests_session():
    token = 'my-token'
    api_base = 'https://my.server/'
    path = '/api/updates/1'

    response = Mock()
    response.raise_for_status = Mock(return_value=None)
    response.json = Mock(return_value=sentinel.resp)

    s = connection.Session(token, api=api_base)
    s.session.get = Mock(return_value=response)

    assert_equal(s.get(path), sentinel.resp)


@istest
def should_retry_failed_requests():
    token = 'my-token'
    api_base = 'https://my.server/'
    path = '/api/updates/1'

    response = Mock()
    response.raise_for_status = Mock(return_value=None)
    response.json = Mock(return_value=sentinel.resp)

    s = connection.Session(token, api=api_base, retry=1)
    s.session.get = Mock(side_effect=[requests.exceptions.HTTPError(), response])

    assert_equal(s.get(path), sentinel.resp)
