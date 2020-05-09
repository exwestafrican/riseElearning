
from comments.views import (
    CommentDetailView
)

from django.urls import re_path


app_name = 'comments'

urlpatterns = [ 

    re_path(r'(?P<slug>\w.+)/(?P<pk>\d+)/$', CommentDetailView.as_view(), name='detail'),
    

 ]

