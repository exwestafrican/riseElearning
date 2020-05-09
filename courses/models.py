from django.db import models
from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import reverse
from django.db.models.signals import pre_save,post_save,pre_delete,post_delete
from .utils import(
     unique_slug_generator,
     slug_generator, 
     file_path,create_unique_name,
     get_class_name
                )
from django.utils.text import slugify
from content.fields import PositionField
from category.models import CourseCategory



User = settings.AUTH_USER_MODEL
# Create your models here.

level_choices= [
    ('clueless','Clueless'), #introductory coruse-tells user what other courses are about
    ('newbie','Newbie'),
    ('got an idea','Got an idea'),
    ('expert','Expert'),
                        ]   


class CourseQuerySet(models.query.QuerySet):
  
    
    def owned_courses(self,user):
        if user.is_authenticated:
            return self.prefetch_related(

                        Prefetch('owned',
                        queryset= MyCourses.objects.filter(user=user),
                        to_attr='is_owner'
                        )
                        
                    )
        else:
            #self is courses.objects.all()
            # return None
            return self


class CourseModelManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model,using=self._db)

    def all(self):
        return self.get_queryset().all()




class Course(models.Model):
    uploaded_by         = models.ForeignKey(User,on_delete=models.CASCADE) #create a signal to set this
    title               = models.CharField(max_length=50,unique=True)
    slug                = models.SlugField(max_length=20,blank=True,null=True)
    course_discription  = models.TextField()
    images              = models.ImageField(upload_to=file_path,null=True,blank=True)
    views               = models.IntegerField(default=0)
    video_count         = models.IntegerField(default=0)
    excersise_count     = models.IntegerField(default=0)
    category            = models.ForeignKey(on_delete=models.CASCADE,to=CourseCategory, related_name='primary_category' )
    other_category      = models.ManyToManyField(to=CourseCategory, related_name='secondary_category',blank=True )
    level               = models.CharField(max_length=100, choices=level_choices)
    number_of_chapters  = models.IntegerField(default=0)
    time_added          = models.DateTimeField(auto_now_add=True)
    free                = models.BooleanField(default = False)
    rating              = models.FloatField(default=0)

    objects         = CourseModelManager()

    #course duration by adding all chapter duration
    #number of videos notes and quizes 
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    def get_purchase_url(self):
        return reverse('courses:purchase', kwargs={'slug': self.slug})

  
class Chapter(models.Model):
    course              = models.ForeignKey(Course,on_delete=models.CASCADE)
    slug                = models.SlugField(null=True, blank=True)
    chapter_name        = models.CharField(max_length=250)
    chapter_number      = models.IntegerField(default=0)
    chapter_description = models.TextField()
    order               = PositionField(collection="course")         # use this order to display week? 
    preivew             = models.CharField(max_length=210,null=True,blank=True)  
    #progress
    #status (choices inprogess,completed)

    #chapter durantion by adding all content duration
    #chapter objective

    def __str__(self):
        return self.chapter_name

    

    @property   #use this in front end view 
    def chapter(self):
        """returns chapter number in a specific format """
        return f'Lesson {self.chapter_number}'
    
    @property
    def course_slug(self):
        """returns slug format of title"""
        return slugify(self.course)
    



    def get_absolute_url(self):
        context = {
            'slug': self.slug,
            # 'chapter_number':slugify(self.chapter),
            # 'course_slug':self.course_slug,
            # 'pk':self.pk
        }
    
        return reverse('courses:chapter_detail', kwargs=context)

    
    class Meta:
        # unique_together = ['chapter', 'title'] old approach
        constraints = [
            models.UniqueConstraint(fields=['course', 'chapter_name'], name ='unique_chapter') #recommended approach
        ]
        ordering = ['order']


class MyCourses(models.Model):
    user                = models.OneToOneField(User,on_delete=models.CASCADE)
    course              = models.ManyToManyField(Course,related_name='owned',blank=True)
    time_added          = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.course.all().count())


    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'MyCourse'
        verbose_name_plural = 'MyCourses'


def post_save_my_course_list(sender,created,instance,*args,**kwargs):
    """
    creates a course profile when a user is created 
    """
    if created:
        MyCourses.objects.get_or_create(user=instance)


post_save.connect(post_save_my_course_list,sender=User)



def pre_save_slug_generator (sender,instance,*args,**kwargs):
    """ 
    generates slug ifslug format of current title is 
    not same as current slug or if slug is none
    """
    title_slug= slugify(instance) #check slug format of current title
    if instance.slug is None or title_slug!=instance.slug:
        instance.slug = slug_generator(instance)
      
pre_save.connect(pre_save_slug_generator,sender=Course)




def post_save_chapter_count(created,sender,instance,*args,**kwargs):
    """ 
    incremeants chapter number and number of course chapter
    by 1 when new chapter is created
    """
  
    if created:
        course_instance = Course.objects.filter(title = instance.course).first() #searches course instnce
        num =course_instance.chapter_set.count()
        instance.chapter_number = num
        course_instance.number_of_chapters = num
        course_instance.save()
        instance.save()
       
post_save.connect(post_save_chapter_count,sender=Chapter)


def pre_delete_chapter_count(sender,instance,*args,**kwargs):
    """ 
    decreases chapter number and number of course chapter
    by 1 when new chapter is deleted
    """
    course_instance = Course.objects.filter(title = instance.course).first() #searches course instnce
    num =course_instance.chapter_set.count()
    instance.chapter_number = num
    course_instance.number_of_chapters = num
    course_instance.save()
    instance.save()
   
pre_delete.connect(pre_delete_chapter_count,sender=Chapter)



def pre_save_chapter_slug_generator (sender,instance,*args,**kwargs):
    """ 
    generates slug if slug format is not 
    same as current slug or if slug is none
    """
    new_slug = slugify(instance.chapter) + "-"+ slugify(instance)
    if instance.slug is None or new_slug!=instance.slug:
        instance.slug  = unique_slug_generator(instance)
     
      
pre_save.connect(pre_save_chapter_slug_generator,sender=Chapter)



def post_save_course_reciver(sender, instance ,created, *args,**kwargs):
    if not instance.category in instance.other_category.all():
        instance.other_category.add(instance.category)
     
       
post_save.connect(post_save_course_reciver,sender=Course)