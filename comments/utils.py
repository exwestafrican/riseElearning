from .models import Comment
from django.shortcuts import redirect
from notification.signals import notify


def notify_comment_or_reply_create(self,comment_form,main_comment,lecture,context,redirect_link=None):
        if main_comment is not None:
            main_comment = int(main_comment)

       
        try:
            main_comment_instance = Comment.objects.get(id=main_comment)
        except Comment.DoesNotExist:
             main_comment = None
        else:
             main_comment = main_comment_instance

        if comment_form.is_valid():
            comment_content = comment_form.cleaned_data['content']
            new_comment = Comment.objects.create_comment(
                 user           = self.request.user,
                 content        = comment_content,
                 path           = lecture.get_comment_path,
                 lecture        = lecture,
                 main_comment   = main_comment
                )

            #get a list of affected users
            affected_users = new_comment.get_affected_users
            print(affected_users)
            if main_comment is None:
                #then it's a question
                creator = context['current_course'].uploaded_by
                
                notify.send(
                    sender=self.request.user, 
                    verb=f"{self.request.user.email} asked a question on {lecture}",
                    action =new_comment,
                    target=lecture,
                    recipient=creator, 
                    affected_users=affected_users
                    )
                   
                
                    
            else:
                #it's a reply 
                recipient = main_comment.user
                notify.send(
                 sender=self.request.user,
                 verb=f"{self.request.user.email} replyed you on {lecture}",
                 action =new_comment,
                 target=lecture,
                 recipient= recipient, 
                 affected_users=affected_users
                 )    

               

                

        if redirect_link:
            return redirect(redirect_link)
        else:
            #i want to see the main comment thread, and not just a reply
            return redirect(main_comment)

