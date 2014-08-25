from django.conf import settings
import django

STATIC_URL = getattr(settings, 'STATIC_URL', settings.MEDIA_URL)
if STATIC_URL == None:
    STATIC_URL = settings.MEDIA_URL
MEDIA_PATH = getattr(settings, 'EDITOR_MEDIA_PATH', '%seditor/' % STATIC_URL)

TREE_INITIAL_STATE = getattr(settings, 'EDITOR_TREE_INITIAL_STATE', 'collapsed')

IS_GRAPPELLI_INSTALLED = 'grappelli' in settings.INSTALLED_APPS


# CATEGORIES_EDITOR_CSS and CATEGORIES_EDITOR_JS
# The admin interface depends on jQuery (http://http://jquery.com) 
# and jQuery.treetable (http://plugins.jquery.com/treetable/).
# 
# If you already include these depencies on your admin pages, awesome! If not,
# set these in your project's settings.py. For example:
#
# CATEGORIES_EDITOR_CSS = {
#     'all': (
#         "css/jquery.treetable.css",
#         "css/jquery.treetable.theme.default.css"
#     ),
# }
# CATEGORIES_EDITOR_JS = (
#     "js/jquery.js",
#     "js/jquery.treetable.js",
# )
#  
CATEGORIES_EDITOR_CSS = getattr(settings, 'CATEGORIES_EDITOR_CSS', {}) 
CATEGORIES_EDITOR_JS = getattr(settings, 'CATEGORIES_EDITOR_JS', [])