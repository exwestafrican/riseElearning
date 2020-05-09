from django.shortcuts import render,Http404,render,redirect
from django.views.generic import ListView,View
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Create your views here.


class AllNotification(LoginRequiredMixin,ListView):
    model                = Notification
    template_name        = 'notification/notification.html'
    context_object_name  = 'notifications'
   
    def get_queryset(self):
       queryset = super(AllNotification, self).get_queryset()
       queryset= Notification.objects.my_notification(user=self.request.user).order_by('-created')
       return queryset


    
class ReadNotifications(View):
    """
    attach a link to all notifications to come here, 
    if it has an absolute url, mark as read and redirect there
    if not, mark as read and redirect to notifications
    """
    def get(self,request,*args,**kwargs):
        sender_object_id = self.kwargs['sender_object_id']
        action_object_id = self.kwargs['action_object_id']
        
        try:
            my_notifications = Notification.objects.filter(
                sender_object_id=sender_object_id,
                action_object_id=action_object_id)
        except Notification.DoesNotExist:
            raise Http404

        else:
            # the same Notification is sent to everyone affected
            for my_notification in my_notifications: 
                if  my_notification.recipient == self.request.user:
                    #only mark my notification as read
                    my_notification.read = True
                    my_notification.save()
                else:
                    pass
            my_notification_action_object = my_notification.action_object
            if  my_notification_action_object is not None:
                return redirect(my_notification_action_object)
            else:
                return redirect(reverse('page_not_fund'))
    
    
    