# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock, Mock
from unittest import main

from link.middleware.core import Middleware
from link.feature import Feature, addfeatures

from link.dbrequest.query import QueryManager, Query

from link.dbrequest.comparison import C
from link.dbrequest.assignment import A
from link.dbrequest.expression import E, F

from link.dbrequest.ast import AST
from link.dbrequest.ast import ASTSingleStatementError
from link.dbrequest.ast import ASTLastStatementError
from link.dbrequest.ast import ASTInvalidStatementError
from link.dbrequest.ast import ASTInvalidFormatError


class QueryManagerTest(UTCase):
    def setUp(self):
        self.inserted_doc = {'_id': 'some id', 'foo': 'bar'}

        self.feature = Mock()

        featurecls = MagicMock(return_value=self.feature)
        featurecls.__class__ = type
        featurecls.name = 'query'
        featurecls.mro = MagicMock(return_value=[Feature])

        cls = type('DummyDriver', (Middleware,), {})
        cls = addfeatures([featurecls])(cls)

        self.query = QueryManager()
        self.query.set_child_middleware(cls())

    def test_all(self):
        q = self.query.all()

        self.assertIsInstance(q, Query)
        self.assertEqual(q.ast, [])
        self.assertEqual(q.result, None)
        self.assertTrue(q.manager is self.query)

    def test_from_ast(self):
        expected = [
            AST(
                'filter',
                AST(
                    'cond_eq', [
                        AST('prop', 'foo'),
                        AST('val', 'bar')
                    ]
                )
            )
        ]

        attrs = {
            'find_elements.return_value': []
        }
        self.feature.configure_mock(**attrs)

        q = self.query.from_ast(expected)

        self.assertIsInstance(q, Query)
        self.assertEqual(q.ast, expected)

        list(q)

        self.feature.find_elements.assert_called_with(expected)

    def test_to_ast(self):
        expected = [
            {
                'name': 'filter',
                'val': {
                    'name': 'cond_eq',
                    'val': [
                        {
                            'name': 'prop',
                            'val': 'foo'
                        },
                        {
                            'name': 'val',
                            'val': 'bar'
                        }
                    ]
                }
            }
        ]

        q = self.query.all().filter(C('foo') == 'bar')

        self.assertEqual(q.to_ast(), expected)

    def test_validate_ast(self):
        with self.assertRaises(ASTSingleStatementError):
            self.query.validate_ast(AST('not_get_or_create', 'unused'))

        for stmt in ['update', 'delete', 'get', 'count', 'group']:
            with self.assertRaises(ASTLastStatementError):
                self.query.validate_ast([
                    AST(stmt, 'unused'),
                    AST('unused', 'unused')
                ])

        with self.assertRaises(ASTInvalidStatementError):
            self.query.validate_ast([
                AST('unknown', 'unused')
            ])

        with self.assertRaises(ASTInvalidFormatError):
            self.query.validate_ast('invalid format')

        self.query.validate_ast([
            AST('filter', 'unused'),
            AST('update', 'unused')
        ])

    def test_manager_get_none(self):
        attrs = {
            'find_elements.return_value': []
        }
        self.feature.configure_mock(**attrs)

        result = self.query.get(C('foo'))

        self.assertIsNone(result)

        self.feature.find_elements.assert_called_with({
            'name': 'cond_exists',
            'val': [
                {
                    'name': 'prop',
                    'val': 'foo'
                },
                {
                    'name': 'val',
                    'val': True
                }
            ]
        })

    def test_manager_get_one(self):
        expected = {'foo': 'bar'}
        attrs = {
            'find_elements.return_value': [expected]
        }
        self.feature.configure_mock(**attrs)

        result = self.query.get(C('foo'))

        self.assertEqual(result, expected)

        self.feature.find_elements.assert_called_with({
            'name': 'cond_exists',
            'val': [
                {
                    'name': 'prop',
                    'val': 'foo'
                },
                {
                    'name': 'val',
                    'val': True
                }
            ]
        })

    def test_manager_create(self):
        expected = {'_id': 'some id', 'foo': 'bar'}
        attrs = {
            'put_element.return_value': expected
        }
        self.feature.configure_mock(**attrs)

        result = self.query.create(A('foo', 'bar'))

        self.assertEqual(result, expected)

        self.feature.put_element.assert_called_with([{
            'name': 'assign',
            'val': [
                {
                    'name': 'prop',
                    'val': 'foo'
                },
                {
                    'name': 'val',
                    'val': 'bar'
                }
            ]
        }])

    def test_query_copy(self):
        q1 = self.query.all()
        q2 = q1._copy()

        self.assertIsInstance(q1, Query)
        self.assertIsInstance(q2, Query)
        self.assertIsNot(q1, q2)

        self.assertIs(q1.manager, q2.manager)
        self.assertEqual(q1.ast, q2.ast)
        self.assertIsNone(q2.result)

    def test_query_count(self):
        attrs = {
            'count_elements.return_value': 3
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all().filter(C('foo') == 'bar').count()

        self.assertEqual(result, 3)

        self.feature.count_elements.assert_called_with([{
            'name': 'filter',
            'val': {
                'name': 'cond_eq',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'foo'
                    },
                    {
                        'name': 'val',
                        'val': 'bar'
                    }
                ]
            }
        }])

    def test_query_get_none(self):
        attrs = {
            'find_elements.return_value': []
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all().get(C('foo'))

        self.assertIsNone(result)

        self.feature.find_elements.assert_called_with([
            {
                'name': 'get',
                'val': {
                    'name': 'cond_exists',
                    'val': [
                        {
                            'name': 'prop',
                            'val': 'foo'
                        },
                        {
                            'name': 'val',
                            'val': True
                        }
                    ]
                }
            }
        ])

    def test_query_get_one(self):
        expected = {'foo': 'bar'}
        attrs = {
            'find_elements.return_value': [expected]
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all().get(C('foo'))

        self.assertEqual(result, expected)

        self.feature.find_elements.assert_called_with([
            {
                'name': 'get',
                'val': {
                    'name': 'cond_exists',
                    'val': [
                        {
                            'name': 'prop',
                            'val': 'foo'
                        },
                        {
                            'name': 'val',
                            'val': True
                        }
                    ]
                }
            }
        ])

    def test_query_filter(self):
        expected = [
            {'_id': 'some id 1', 'foo': 'bar'},
            {'_id': 'some id 2', 'foo': 'bar'},
            {'_id': 'some id 3', 'foo': 'bar'}
        ]
        attrs = {
            'find_elements.return_value': expected
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all().filter(C('foo') == 'bar')

        self.assertIsInstance(result, Query)

        result = list(result)
        self.assertEqual(result, expected)

        self.feature.find_elements.assert_called_with([
            {
                'name': 'filter',
                'val': {
                    'name': 'cond_eq',
                    'val': [
                        {
                            'name': 'prop',
                            'val': 'foo'
                        },
                        {
                            'name': 'val',
                            'val': 'bar'
                        }
                    ]
                }
            }
        ])

    def test_query_exclude(self):
        expected = [
            {'_id': 'some id 1', 'foo': 'baz'},
            {'_id': 'some id 2', 'foo': 'baz'},
            {'_id': 'some id 3', 'foo': 'baz'}
        ]
        attrs = {
            'find_elements.return_value': expected
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all().exclude(C('foo') == 'bar')

        self.assertIsInstance(result, Query)

        result = list(result)
        self.assertEqual(result, expected)

        self.feature.find_elements.assert_called_with([
            {
                'name': 'exclude',
                'val': {
                    'name': 'cond_eq',
                    'val': [
                        {
                            'name': 'prop',
                            'val': 'foo'
                        },
                        {
                            'name': 'val',
                            'val': 'bar'
                        }
                    ]
                }
            }
        ])

    def test_query_slice(self):
        expected = [
            {'_id': 'some id 2', 'foo': 'bar'},
            {'_id': 'some id 3', 'foo': 'bar'}
        ]
        attrs = {
            'find_elements.return_value': expected
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all()[1:2]

        self.assertIsInstance(result, Query)

        result = list(result)
        self.assertEqual(result, expected)

        self.feature.find_elements.assert_called_with([
            {
                'name': 'slice',
                'val': slice(1, 2)
            }
        ])

    def test_query_cache(self):
        expected = [
            {'_id': 'some id 1', 'foo': 'bar'},
            {'_id': 'some id 2', 'foo': 'bar'},
            {'_id': 'some id 3', 'foo': 'bar'}
        ]
        attrs = {
            'find_elements.return_value': expected
        }
        self.feature.configure_mock(**attrs)

        query = self.query.all()

        self.assertIsInstance(query, Query)

        result1 = list(query)
        self.assertEqual(result1, expected)

        result2 = list(query)
        self.assertEqual(result2, expected)

        self.feature.find_elements.assert_called_once_with([])

    def test_query_update(self):
        attrs = {
            'update_elements.return_value': 3
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all().update(A('foo', 'bar'))

        self.assertEqual(result, 3)
        self.feature.update_elements.assert_called_with([], [
            {
                'name': 'assign',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'foo'
                    },
                    {
                        'name': 'val',
                        'val': 'bar'
                    }
                ]
            }
        ])

    def test_query_delete(self):
        attrs = {
            'remove_elements.return_value': 3
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all().delete()

        self.assertEqual(result, 3)
        self.feature.remove_elements.assert_called_with([])

    def test_query_group(self):
        expected = {'foo': ['bar', 'baz', 'biz']}
        attrs = {
            'find_elements.return_value': expected
        }
        self.feature.configure_mock(**attrs)

        result = self.query.all().group('foo', F('sum', E('bar')))

        self.assertEqual(result, expected)

        self.feature.find_elements.assert_called_with([
            {
                'name': 'group',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'foo'
                    },
                    {
                        'name': 'func_sum',
                        'val': [
                            {
                                'name': 'ref',
                                'val': 'bar'
                            }
                        ]
                    }
                ]
            }
        ])


if __name__ == '__main__':
    main()
