
from category.views import (
     CourseCategoryListView,
     CourseCategoryDetailView
)

from django.urls import re_path


app_name = 'category'

urlpatterns = [
    re_path(r'^$', CourseCategoryListView.as_view(), name='list'),
    
    re_path(r'(?P<slug>\w.+)$', CourseCategoryDetailView.as_view(), name='detail'),

    
 ]