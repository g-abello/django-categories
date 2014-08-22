from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from django.db.models import Q
from django.test import TestCase

from categories.models import (
    _category_relation_models,
    Category,
    CategoryRelation,
)
from .helpers import assert_equal_Qs


class CategoriesModelsTestCase(unittest.TestCase):

    # _category_relation_models returns a single Q object made by ORing together
    # the passed in Qs. Returns {} if passed an empty list.
    #
    def test__category_relation_models(self):
        Qs = [
            Q(app_label="test_app", model="one_model"),
            Q(app_label="test_app", model="two_model"),
        ]
        assert_equal_Qs(Qs[0] | Qs[1], _category_relation_models(Qs))
    
    def test__category_relation_models_empty_list(self):
        self.assertEqual({}, _category_relation_models([]))


class CategoryDjangoTestCase(TestCase):

    # Category.objects.active() only returns categories that are active.
    #
    def test_objects_active(self):
        category = Category.create(active=True)
        self.assertEqual(
            category,
            Category.objects.active().get(pk=category.pk)
        )

    def test_objects_active_exclude_inactive_category(self):
        category = Category.create(active=False)
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.active().get(pk=category.pk)

    # Category.get_absolute_url returns a `/` separated url path to the Category
    # based on its ancestors slugs or the Category's alternate_url if present.
    #
    def test_get_absolute_url(self):
        ancestor = Category.create(slug="Ancestor")
        category = Category.create(slug="Category", parent=ancestor)
        self.assertEqual(
            "/categories/Ancestor/Category/",
            category.get_absolute_url()
        )

    def test_get_absolute_url_alternate_url(self):
        category = Category(alternate_url="http://www.test.com/alt_url")
        self.assertEqual(
            "http://www.test.com/alt_url",
            category.get_absolute_url()
        )

    # Category.__unicode__ returns a string with the name of the Category
    # and all of its ancestors seperated by " > ".
    #
    def test___unicode__(self):
        ancestor = Category.create(name="Ancestor")
        category = Category.create(name="Category", parent=ancestor)
        self.assertEqual("Ancestor > Category", category.__unicode__())

    def test___unicode__no_ancestors(self):
        self.assertEqual("Category", Category(name="Category").__unicode__())


class CategoryRelationTestCase(unittest.TestCase):

    # CategoryRelation.__unicode__ returns a simple text representation of
    # CategoryRelation.
    #
    def test___unicode__(self):
        category_relation = CategoryRelation()
        self.assertEqual("CategoryRelation", str(category_relation))
