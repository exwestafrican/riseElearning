from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView, 
)
from django.views.generic.base import RedirectView
from .models import Course, Chapter, MyCourses
from .mixings import MemberRequiredMixing
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseForm
from django.urls import reverse_lazy
from django.conf import settings
from django.db.models import Prefetch
# from .utils import generate_profile
from social.models import UserProfile
from content.models import Contents
from django.http import Http404
# Create your views here.


class CourseListView(ListView):
    queryset = Course.objects.order_by('-time_added')
    paginate_by = 10
    context_object_name = 'courses'
    template_name= 'courses/list.html'
 

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(UserProfile,user=self.request.user)
        context['profile']= profile
        return context
    
    
 


class CourseDetailView(DetailView):
    queryset = Course.objects.all()
    context_object_name = 'course'
    template_name= 'courses/detail.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(UserProfile,user=self.request.user)
        context['profile']= profile
        return context
    

    


#edit this
class CoursePurchaseRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'courses:detail'

    def get_redirect_url(self,*args,**kwargs):
        bought_course = get_object_or_404(Course,slug=kwargs['slug']) #get the bought course
        user_courses = MyCourses.objects.get(user=self.request.user)
        user_courses.course.add(bought_course) #add it to users list of courses
        return super().get_redirect_url(*args, **kwargs)


class ChapterDetailView(DetailView):
    model = Chapter
    


class CourseCreateView(CreateView): #make sure only staffs can create this 
    model = Course
    form_class = CourseForm
    template_name = "courses/create.html"
    # success_url = reverse_lazy('Course:detail')
    
    

    
    def form_valid(self,form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        model_instance = form.save(commit=False)
        model_instance.user = self.request.user
        model_instance.save()
        return super().form_valid(form)
