from search.views import search_view

from django.urls import re_path

app_name = 'search'

urlpatterns = [
    re_path(r'^$', search_view, name='query'),
    
    
 ]
