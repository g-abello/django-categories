# Test discovery in Django 1.4 and 1.5 looks for test cases in the `tests`
# module. So we include all of our tests here for those versions to discover.
#
# In Django 1.6, files matching `test*.py` are discovered and run. Maybe we
# won't need these in the future.
# 
from categories.tests.test_category_import import *
from categories.tests.test_models import *
from categories.tests.test_registration import *
from categories.tests.test_templatetags import *