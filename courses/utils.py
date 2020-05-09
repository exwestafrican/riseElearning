from django.utils.text import slugify
import random,string
import os 
from django.shortcuts import get_object_or_404
# from social.models import UserProfile


def slug_generator(instance,*args,**kwargs):
    """takes unique title and generates a slug"""

    title = instance.title      
    slug_title = slugify(title) #converts title to slug
    return slug_title

def alpha_numeric_generator(suffix=None,size=3):
    alpha_numeric=[random.choice(string.ascii_lowercase+string.digits) for _ in range(size)]
    if suffix:
        return suffix+"".join(alpha_numeric)
    return "".join(alpha_numeric)


def query_check(instance,new_slug,*args,**kwargs):
    model_class = instance.__class__ #generates class name of model
    queryset = model_class.objects.filter(slug=new_slug)
    while queryset.exists():
        new_slug= new_slug + "-"+ alpha_numeric_generator()
        queryset = model_class.objects.filter(slug=new_slug)
    return new_slug
    

def unique_slug_generator(instance,*args,**kwargs):
    """takes chapter title and number,generates a slug and checks if slug is unique"""
    new_slug = slugify(instance.chapter)+ "-"+slugify(instance.chapter_name)
    return query_check(instance,new_slug=new_slug)
   
    
def get_file_extention(filepath):
    """ gets extension from uploaded file"""
    fileroot , file_ext = os.path.splitext(filepath)
    return fileroot , file_ext

def get_class_name(self): 
    """ takes the class path and returns the class name"""
    model_class_path =str(self.__class__).split(".") #returns a format <class 'courses.models.Course'>
    path_split = model_class_path[-1].split("'") #splits ' and returns ["<class 'courses", 'models', "Course'>"]
    klass_name = path_split [0] #takes the first item in a split 
    return klass_name


def file_path(self,filename):
    """ 
    creates a new_file name , checks if it exist, 
    then creates and alternative name
    """
    new_file_name = self.title
    fileroot,file_ext = get_file_extention(filename)  #gets extension from uploaded file
    new_name = get_class_name(self)+"/"+slugify(new_file_name)+file_ext #generates a new url path for file and adds extension
    return create_unique_name(self,filename=new_name)


def create_unique_name(self,filename):
    model_class =self.__class__
    qs = model_class.objects.filter(images__iexact=filename)
    if qs.exists():
        rand_num =random.randint(1,400)
        fileroot,file_ext = get_file_extention(filename)
        alt_name =  get_class_name(self)+"/"+ filename + str(rand_num) + file_ext #greates a alternative name if file exists
        return create_unique_name(self,filename=alt_name)
    return filename


# def generate_profile(self,*args,**kwargs):
#     profile=None
#     user=self.request.user
#     if user.is_authenticated:
#         profile = get_object_or_404(UserProfile,user=user)  
#     return profile


def get_content_or_None(content_chapter):
    try:
        content_chapter.contents_set.all().first() 
    except AttributeError:
        content_chapter   = None
        return content_chapter
    else:
        content_chapter  = content_chapter.contents_set.all().first()  
        return content_chapter


   