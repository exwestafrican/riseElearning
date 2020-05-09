from django.db import models
from courses.utils import slug_generator, unique_slug_generator
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse
from courses.models import Chapter, Course
from .fields import PositionField
from courses.utils import get_file_extention,get_class_name,query_check
import random , urllib.parse
from django.conf import settings
from notification.models import TaggedItem
from django.contrib.contenttypes.fields import GenericRelation


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
    qs = model_class.objects.filter(lecture__iexact=filename)
    if qs.exists():
        rand_num =random.randint(1,400)
        fileroot,file_ext = get_file_extention(filename)
        alt_name =  get_class_name(self)+"/"+ filename + str(rand_num) + file_ext #greates a alternative name if file exists
        return create_unique_name(self,filename=alt_name)
    return filename


def content_slug_generator(instance,*args,**kwargs):
    """takes chapter title and number,generates a slug and checks if slug is unique"""
    new_slug = slugify(instance.chapter)+ "-"+slugify(instance.title)
    return query_check(instance,new_slug=new_slug)



lesson_material= [
    ('video','Video'),
    ('slide','Slide'),
    ('excersise','Excerise'),
    ('notes','Notes'),
                        ]



class ContentsQuerySet(models.query.QuerySet):
  
    
    def related_chapters(self):
            return self.select_related("chapter")
                        
                   
       


class ContentsModelManager(models.Manager):
    def get_queryset(self):
        return ContentsQuerySet(self.model,using=self._db)

    def all(self):
        return self.get_queryset().all()
    
   

DEFAULT_MESSAGE= "Learn more with Rise Elearning at"


# Create your models here.
class Contents(models.Model): #rename this lecture
   
    course              = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,blank=True) #consider setting this null
    chapter             = models.ForeignKey(Chapter,on_delete=models.SET_NULL,null=True ,blank=True)
    slug                = models.SlugField(null=True, blank=True)
    title               = models.CharField(max_length=150) #create validation to make title unique to lecture
    lesson_type         =  models.CharField(max_length=100, choices=lesson_material ,default='video')
    #uplaod a file as content 
    tags                = GenericRelation(TaggedItem,null=True,blank=True)
    preview             = models.BooleanField(default=False)
    share_message       = models.CharField(max_length=150,default=DEFAULT_MESSAGE)
    last_saved          = models.DateTimeField(auto_now=True)
    lecture             = models.FileField(null=True, blank=True,upload_to=file_path)
    #we need to order this 
    order               = PositionField(collection='chapter')
    #add duration
    objects             = ContentsModelManager()

    #create content model add content, when a movie finishes java script pops up a box i click and it adds content to model

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'

        constraints = [
            models.UniqueConstraint(fields=['chapter', 'title'], name ='unique_lesson') #recommended approach
        ]
        ordering = ['order']


    def __str__(self):
        return self.title

    

    #content/course_name/chapter_number/title
    def get_absolute_url(self):
        context = {
            'slug': self.slug,
            "lesson_type":slugify(self.lesson_type)
        }
       
        return reverse('content:content_detail', kwargs=context)

    
    def get_share_message(self):
        full_url ="https://"+ settings.FULL_DOMAIN_NAME+self.get_absolute_url()
        msg_and_url = self.share_message + " " + full_url
        return urllib.parse.quote(msg_and_url)
   

    @property
    def get_comment_path(self):
        full_url ="https://"+ settings.FULL_DOMAIN_NAME+self.get_absolute_url()
        return full_url



def pre_save_content_slug_generator (sender,instance,*args,**kwargs):
    """ 
    generates slug ifslug format of current title is 
    not same as current slug or if slug is none

    """
    title_slug= slugify(instance.chapter)+ "-"+slugify(instance.title) #check slug format of current title
    if instance.slug is None or title_slug!=instance.slug:
        instance.slug =  content_slug_generator(instance)
    instance.slug = title_slug   
pre_save.connect(pre_save_content_slug_generator,sender=Contents)



def course_content_connector (sender,instance,*args,**kwargs):
    chapter = Chapter.objects.filter(chapter_name=instance.chapter).select_related('course').first()
    instance.course = chapter.course
   

pre_save.connect(course_content_connector,sender=Contents)


# from moviepy.editor import VideoFileClip
# clip = VideoFileClip()
# print( clip.duration )


# print(Contents.objects.all()[2])