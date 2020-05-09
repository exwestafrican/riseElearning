from django.shortcuts import render 
from .models import CourseCategory
from django.db.models import Count, Q
from courses.models import Course
from django.views.generic import ListView , DetailView , View
from django.core.paginator import Paginator
# Create your views here.


class CourseCategoryListView(ListView):
    queryset= CourseCategory.objects.all().order_by('name')
    template_name= 'category/list.html'
    context_object_name= 'course_category'
    

  

class CourseCategoryDetailView(DetailView):
    queryset = CourseCategory.objects.all()
    context_object_name = 'category'
    template_name= 'category/detail.html'
    
    def get_context_data(self, *args,**kwargs):
        context = super(CourseCategoryDetailView, self).get_context_data(**kwargs)

        name=context.get('category')
        user = self.request.user
        
        queryset   =Course.objects.filter(
            Q(other_category__name=name) | Q(category__name=name)

            ) 

            

        if user.is_authenticated:
       
            queryset=queryset.owned_courses(user=user).distinct()
            
        # paginator = Paginator(queryset, 5)
        # print(paginator)
        context['courses']= queryset
       
   
        return context
    



    
  