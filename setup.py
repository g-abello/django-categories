from setuptools import setup, find_packages
import django
import categories
import os

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

try:
    if float(django.get_version()) < 1.7:
        print "version antiguaa"
        reqs = open(os.path.join(os.path.dirname(__file__), 'requirements/old_versions.txt')).read().splitlines()
    else:
        print "Django 1.7!"
        reqs = open(os.path.join(os.path.dirname(__file__), 'requirements/base.txt')).read().splitlines()
except (IOError, OSError):
    reqs = ''
print "reqs = ", reqs

setup(
    name='django-categories',
    version=categories.get_version(),
    description='A way to handle one or more hierarchical category trees in django.',
    long_description=long_description,
    author='Chapman Shoop',
    author_email='chapman.shoop@gmail.com',
    include_package_data=True,
    url='http://github.com/rbgb/django-categories',
    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
    ],
    install_requires = reqs,
    dependency_links = []
)
