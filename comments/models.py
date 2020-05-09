from django.db import models
from django.conf import settings
from content.models import Contents
from django.shortcuts import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save

# Create your models here.
User = settings.AUTH_USER_MODEL
class CommentQuerySet(models.QuerySet):
    def all(self):
        #where main comment = None tells me it's a question not a reply
        return self.filter(main_comment=None)


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().all()

    def create_comment(self,user,content,path,lecture,main_comment=None):
        if not path:
            raise ValueError('include a path when adding a comment')
        if not user:
            raise ValueError('include a user when adding a comment')

        Comment = self.model(
            user    = user,
            path    = path,
            content = content,
            lecture = lecture,
        ) 

        if main_comment is not None:
            Comment.main_comment = main_comment
        Comment.save(using=self._db)
        return Comment

class Comment(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    content      = models.TextField()
    main_comment = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    path         = models.CharField(max_length=400)
    lecture      = models.ForeignKey(Contents,on_delete=models.CASCADE,null=True,blank=True)    
    slug         = models.SlugField(max_length=400,null=True,blank=True)
    updated      = models.DateTimeField(auto_now=True)
    created      = models.DateTimeField(auto_now_add = True)

    objects = CommentManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.main_comment is None:
             return f'{self.user.email} made a comment on {self.lecture}'
        return f'{self.user.email} replied a comment on {self.lecture}'

    @property
    def get_comment(self):
        return self.content

    def is_reply(self):
        if self.main_comment is None:
           #if there is no main comment then comment is main comment
           return False
        return True #if there is a main comment, then comment is a reply

    @property
    def get_affected_users(self):
        affected_users = set()
        if self.is_reply():
            main_comment = self.main_comment #find main comment
            replies = self.__class__.objects.filter(main_comment=main_comment) #find all replies
            for reply in replies:
                affected_users.add(reply.user) #only unique users
            return affected_users

        #if it's not reply, notifiy course instructor    
        return None 
           
            

    @property
    def comment_replies(self):
        if self.is_reply():
            return None
        return self.__class__.objects.filter(main_comment=self) #return all the comments (replies) where main comment is this comment

    @property
    def comment_content(self):
        return self.content
    
    def get_absolute_url(self):
        context = {
            'slug':slugify(self.lecture),
            'pk': self.pk,
                
        }
        
        return reverse('comments:detail', kwargs=context)




def post_save_comment_slug(created,sender,instance,*args,**kwargs):
    """ 
    creates a slug if slug field is empty or a new comment is created
    """
    if created or instance.slug is None:
        instance.slug = slugify(instance.lecture)
        instance.save()

    
      
post_save.connect(post_save_comment_slug,sender=Comment)