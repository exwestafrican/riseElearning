from django.db import models
from .signals import notify
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse


User = settings.AUTH_USER_MODEL
TEST_CHOICES =[
    ('choice 1','choice 1'),
    ('choice 2','choice 2'),
    ('choice 3','choice 3'),
]
# Create your models here.
class TaggedItem(models.Model):
    tag = models.SlugField(choices=TEST_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag


class NotificationQuerySet(models.QuerySet):
    def my_notification(self,user):
        return self.filter(recipient=user)
    
    def read_notification(self):
        return self.filter(read=True)
    
    def unread_notification(self):
        return self.filter(read=False)

class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def my_notification(self,user):
        return self.get_queryset().my_notification(user)

    def read_notification(self):
        return self.get_queryset().my_notification(user).read_notification()

    def unread_notification(self):
        return self.get_queryset().my_notification(user).unread_notification() 


class Notification(models.Model):
    sender_content_type = models.ForeignKey(
            ContentType, 
            on_delete=models.CASCADE,
            related_name="sender"  ) #tumise (a user)

    sender_object_id = models.PositiveIntegerField()
    sender_object = GenericForeignKey('sender_content_type', 'sender_object_id')
        

    verb  = models.CharField(max_length=250) #commented  (what did he do)

    
    action_content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name="action",
        null=True,
        blank = True,
        )

    action_object_id = models.PositiveIntegerField(null=True,blank=True)
    action_object = GenericForeignKey('action_content_type','action_object_id')  #with a comment (instance of a model) (object of the verb)



    
    target_content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name="target",
        null=True,
        blank = True
        )
    target_object_id = models.PositiveIntegerField(null=True,blank=True)
    target_object = GenericForeignKey('target_content_type','target_object_id') # on a video (an instance of a model)

        
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    read      = models.BooleanField(default=False)
    created   = models.DateTimeField(auto_now=True)

    objects  = NotificationManager()

    def __str__(self):
        return self.verb

    def get_absolute_url(self):
        context = {
            'sender_object_id':self.sender_object_id,
            'action_object_id': self.action_object_id,       
        }
        
        return reverse('notification:read', kwargs=context)



def new_notification_alert(*args,**kwargs):
   
    sender          = kwargs.pop('sender')
    verb            = kwargs.pop('verb')
    recipient       = kwargs.pop('recipient')
    affected_users  = kwargs.pop('affected_users')

    print(f"recipient is {recipient}")
    print(f"sender is {sender}")
    
    if affected_users:
       affected_users.add(recipient) #include the recipient
       for affected_user in affected_users:
            if sender is affected_user:
                # don't need to send commenter a notificiation he or she commented
                pass
            else:
                new_notification = Notification(
                    sender_content_type=ContentType.objects.get_for_model(sender),
                    sender_object_id= sender.id,
                    verb=verb,
                    recipient=affected_user,
                )
                
            
                for options in ["action","target"]:
            
                    # option_value = kwargs.pop(options,None)
                    option_value = kwargs.get(options)
                
                    if option_value is not None:
                        
                        setattr(new_notification, f'{options}_content_type', ContentType.objects.get_for_model(option_value) )
                        setattr(new_notification, f'{options}_object_id', option_value.id )
                        # setattr(p, 'age', 23)
                        # p.age = 23

                    new_notification.save()

    else:
                new_notification = Notification(
                    sender_content_type=ContentType.objects.get_for_model(sender),
                    sender_object_id= sender.id,
                    verb=verb,
                    recipient=recipient,
                )
                
            
                for options in ["action","target"]:
            
                    # option_value = kwargs.pop(options,None)
                    option_value = kwargs.get(options)
                
                    if option_value is not None:
                        
                        setattr(new_notification, f'{options}_content_type', ContentType.objects.get_for_model(option_value) )
                        setattr(new_notification, f'{options}_object_id', option_value.id )
                        # setattr(p, 'age', 23)
                        # p.age = 23         
                   
                    new_notification.save()


notify.connect(new_notification_alert)