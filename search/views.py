from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.db.models import Q
from courses.models import Course, Chapter
from content.models import Contents
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from social.models import UserProfile
# Create your views here.


def search_view(request,*args,**kwargs):
    courses = None
    page_obj = None
    search_input = request.GET.get('q')

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile,user=request.user) 
    else:
        user_profile=None 

    search_input=str(search_input)

    if search_input:
            courses = Course.objects.filter(
                Q(title__icontains = search_input)|
                Q(course_discription = search_input)|
                Q(category__name__icontains = search_input)|
                Q(other_category__name__icontains = search_input)
            ).distinct()

            content = Contents.objects.filter(
                    Q(title__icontains = search_input)
            ).prefetch_related("chapter")
        

            if content:  #if a user searches a content, return the course 
                for obj in content:
                    obj.chapter
                    content_in_course = Course.objects.filter(
                        chapter=obj.chapter).distinct()

              
                # courses = (courses|content_in_course)
                
                courses = courses.union(content_in_course) #sometimes buggy- fixed
               
             
            paginator = Paginator(courses, 4) # Show 10 courses per page.
            page_number = request.GET.get('page')
            
            try:
                page_obj = paginator.get_page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.get_page(1)
            except EmptyPage:
                page_obj = paginator.get_page(paginator.num_pages)
            except:
                page_obj = paginator.get_page(1)
           
    context = {
                
                'courses': courses,
                "search_input":search_input,
                'page_obj': page_obj,
                'profile': user_profile,
               
            }

    return render(request, 'search/search_query.html', context)
 