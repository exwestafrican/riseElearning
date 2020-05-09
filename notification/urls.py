from django.urls import re_path
from notification.views import AllNotification,ReadNotifications

app_name = 'notification'

urlpatterns = [
   
    
    # re_path(r'^unread$',AllNotification.as_view(),name='all_notifications'),
    re_path(r'^all/$',AllNotification.as_view(),name='all_notifications'),
    re_path(r'read/(?P<sender_object_id>\d+)/(?P<action_object_id>\d+)/$', ReadNotifications.as_view(), name='read'),
    
    # re_path(r'^read$',AllNotification.as_view(),name='all_notifications'),
]