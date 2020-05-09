from courses.views import (
    CourseListView, 
    CourseDetailView ,
    ChapterDetailView,
    CourseCreateView,
    CoursePurchaseRedirectView,
)

from django.urls import re_path

app_name = 'courses'

urlpatterns = [
    re_path(r'^$', CourseListView.as_view(), name='list'),
    re_path(r'create/$',CourseCreateView.as_view(),name='create'),  
    re_path(r'^(?P<slug>\w.+)/$',ChapterDetailView.as_view(),name='chapter_detail'), #need a lecture slug
    re_path(r'(?P<slug>\w.+)/purchase$',CoursePurchaseRedirectView.as_view(),name='purchase'),
    re_path(r'(?P<slug>\w.+)$',CourseDetailView.as_view(),name='detail'),
    

    
 ]




#trail
# re_path(r'^(?P<slug>\w.+)$', CourseDetailView.as_view(), name='detail'),
# re_path(r'(?P<pk>\d+)$',ChapterDetailView.as_view(),name='chapter_detail'),
# re_path(r'^(?P<course_slug>\w.+)/(?P<slug>\w.+)$',
    #                      ChapterDetailView.as_view(),name='chapter_detail'),