# from courses.models import Course
# import random, string

# def create_multiple_items(title_lenght=10,quereyset=Course.objects.all()):
#     count = 0
#     while count < 20:
        
#         for courses_ in quereyset:
#             my_list = [ random.choice(string.ascii_lowercase) for _ in range(title_lenght)] 
#             new_title = "".join(my_list)

#             uploaded_by         = courses_.uploaded_by
#             title               = new_title
#             course_discription  = courses_.course_discription
#             images              = courses_.images  
#             category            = courses_.category
#             other_category      = courses_.other_category
#             level               = courses_.level
#             price               = courses_.price
#             new_course = Course.objects.create(
#                         uploaded_by         = uploaded_by,
#                         title               = title ,      
#                         course_discription  = courses_.course_discription,
#                         images              = images  ,
#                         category            = category,
#                         level               = level,
#                         price               = price

#                         )
           
#             count += 1     
#     return  count

   
import re


# def first_number(word):
#     return re.search(r'\d',word)


# g= first_number("de1le")

# print(g)


def find_emails(emails):
    return re.findall(r'[+\w\d.-]+@[.\w]+',emails)


emails = 'kenneth@teamtreehouse.com, @kennethlove, @chalkers, rew+gotcha@teamtreehouse.com , exa.mple@example.co.uk'


found_emails = find_emails(emails=emails)

print(found_emails)


# class CourseCategoryDetailView(ListView):
#     paginate_by = 2
#     model = CourseCategory
#     # queryset= CourseCategory.objects.all().order_by('name')
#     # context_object_name= 'course_category'
#     # template_name= 'category/detail.html'
    
    
    
#     def get (self,request,*args,**kwargs):
        
#         name = self.kwargs['slug']
#         name = name.split("-")
#         name = " ".join(name)
#         print(name)
#         user = self.request.user
        
#         queryset   =Course.objects.filter(
#             Q(other_category__name__iexact=name) | Q(category__name__iexact=name)

#             ) 

#         # print(queryset)
            

#         if user.is_authenticated:
       
#             queryset=queryset.owned_courses(user=user).distinct()

            
#         context = {
#             'courses' : queryset,
#             "category": name
#         }
       
#         return render(request,'category/detail.html',context)


