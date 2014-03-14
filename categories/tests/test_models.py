from django.test import TestCase
from categories.models import Category


class CategoryTestCase(TestCase):

    # Category.objects.active() only returns categories that are active.
    #
    def test_objects_active_inlcudes_active_category(self):
        category = Category.create(active=False)
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.active().get(pk=category.pk)

    def test_objects_active_excludes_inactive_category(self):
        category = Category.create(active=True)
        self.assertEqual(
            category,
            Category.objects.active().get(pk=category.pk)
        )
