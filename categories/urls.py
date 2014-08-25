# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from .models import Category


categorytree_dict = {
    'queryset': Category.objects.filter(level=0)
}

urlpatterns = patterns('',
    url(
        r'^$', ListView.as_view(**categorytree_dict), name='categories_tree_list'
    ),
)

urlpatterns += patterns('categories.views',
    url(r'^(?P<path>.+)/$', 'category_detail', name='categories_category'),
)
