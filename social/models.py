from datetime import datetime,timezone
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.contrib.auth import user_logged_in
from django.utils import timezone
from enrolment.models import Membership



# from courses.models import Course
# Create your models here.

User = settings.AUTH_USER_MODEL

#automatically create this at sign up
class UserProfile(models.Model):
    user                  = models.OneToOneField(User,on_delete=models.CASCADE)
    is_member             = models.BooleanField(default=False)
    bio                   = models.CharField(null=True , blank=True, max_length=50)



    def __str__(self):
        return self.user.username


    def update_user_membership_profile(self): #add this when the user clicks to play a video
        """ 
        check if a user is a member 
        and if membership has expired
        """
  
        request_user = Membership.objects.get(user=self.user)
    

        if  self.user.is_staff:
            # simplest answer, every staff is a member
            self.is_member = True

        if self.is_member:
            if datetime.now(timezone.utc) > request_user.membership_end_date:
                self.is_member = False
                

        if not self.is_member:
            if datetime.now(timezone.utc) <= request_user.membership_end_date:
                self.is_member = True
    

        self.save()

    # def generate_profile(self,*args,**kwargs):
    #     profile=None
    #     if user.is_authenticated:
    #         profile = self.objects.get
    #         get_object_or_404(self.__class__,user=user)  
    #     return profile

   

# class CourseLikes (models.Model):
#     user    = models.OneToOneField(User,on_delete=models.CASCADE)
#     course  = models.ForeignKey(Course,on_delete=models.CASCADE)



def post_save_create_user_and_membership_profile(created,sender,instance,*args,**kwargs):
    """ 
    activates a user profile once a user is created
    """
    if created:
        UserProfile.objects.create(user=instance)
        Membership.objects.create(user=instance)

    
post_save.connect(post_save_create_user_and_membership_profile,sender=User)



def post_membership_save_status_update(sender,instance,created,*args,**kwargs):
    """ updates membership once profile is created  or edited """

    user_profile = UserProfile.objects.get(user=instance.user)
    user_profile.update_user_membership_profile()

post_save.connect(post_membership_save_status_update,sender=Membership)




def check_user_membership_status(sender,request,user,*args,**kwargs):
    #if user can log in, then profile was created

    #update users membership once user logs in

    loged_in_user_profile = UserProfile.objects.get(user=user)
    loged_in_user_profile.update_user_membership_profile()
  

user_logged_in.connect(check_user_membership_status)