from django.urls import re_path
from content.views import ContentsDetailView

app_name = 'content'

urlpatterns = [
   
    re_path(r'^(?P<slug>\w.+)/(?P<lesson_type>\w.+)$',
                         ContentsDetailView.as_view(),name='content_detail'), #need a lecture slug
]