from django.db import models
from django.shortcuts import reverse
from django.db.models import Count
from django.db.models.signals import pre_save
from django.utils.text import slugify


# Create your models here.


class CourseCategoryQuerySet(models.query.QuerySet):
     def active(self):
        return self.filter(active=True)
    
     


class CourseCategoryModelManager(models.Manager):
    def get_queryset(self):
        return CourseCategoryQuerySet(self.model,using=self._db)
  
    def all(self):
        return self.get_queryset().all(

        ).active().annotate(
           courses_lenght=Count("seconday_category",distinct=True)
        ).prefetch_related("primary_category","seconday_category")


class CourseCategory(models.Model):
    name     = models.CharField(max_length=100, unique=True)
    slug     = models.SlugField(max_length=100)
    active   = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category:detail', kwargs={'slug': self.slug})


    
def pre_save_course_category_slug_generator(sender,instance,*args,**kwargs):
    slug= slugify(instance.name) #check slug format of current title
    if instance.slug is None or slug!=instance.slug:
        instance.slug = slugify(instance.name)
       


pre_save.connect(pre_save_course_category_slug_generator,sender=CourseCategory)





   

