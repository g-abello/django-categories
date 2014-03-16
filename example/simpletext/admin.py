from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from django.contrib import admin

from categories.admin import CategoryBaseAdmin, CategoryBaseAdminForm

from .models import SimpleText, SimpleCategory


class SimpleTextAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'description', )
        }),
    )
admin.site.register(SimpleText, SimpleTextAdmin)

class SimpleCategoryAdminForm(CategoryBaseAdminForm):
    class Meta:
        model = SimpleCategory


class SimpleCategoryAdmin(CategoryBaseAdmin):
    form = SimpleCategoryAdminForm
admin.site.register(SimpleCategory, SimpleCategoryAdmin)
