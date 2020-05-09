from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from .models import Comment
from django.conf import settings
from django.http import Http404
from courses.utils import get_content_or_None
from social.models import UserProfile
from comments.forms import CommentForm
from content.models import Contents
from courses.models import Course,Chapter,MyCourses
from notification.signals import notify
from comments.forms import CommentForm
from .utils import notify_comment_or_reply_create



# Create your views here.


class CommentDetailView(View):
    form_class = CommentForm

    def load_context(self):
        # profile= generate_profile(self)
        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(UserProfile,user=self.request.user)
        user = self.request.user

        pk = self.kwargs['pk']
        slug = self.kwargs['slug']
        lecture =  slug.split('-')
        lecture =  " ".join(lecture)

      
    
 
        try:
            content = Contents.objects.get_queryset().related_chapters().get(title__icontains=lecture)

          
        except Contents.DoesNotExist:
                raise Http404

        else:
            # do not take anyone to the next chapter if they are not a member 
            chapter             = content.chapter
            chapterNumber       = chapter.chapter_number  
            contents            = chapter.contents_set.all()
           
            next_chapter        = Chapter.objects.filter(chapter_number=chapterNumber+1,course=chapter.course).prefetch_related('contents_set').first()
           
            next_content        = get_content_or_None(content_chapter=next_chapter)
     
            previous_chapter    = Chapter.objects.filter(chapter_number=chapterNumber-1,course=chapter.course).first()
            previous_content    = get_content_or_None(content_chapter=previous_chapter)
            
            comment             = Comment.objects.get(id=pk)

            if comment.main_comment is None:
                #need this to display both questions and all replies
                # means it's a question
                main_comment        = comment
            else:
                main_comment        = comment.main_comment

            
            
           
            current_course      = content.course
            # number_of_replies   = Comment.objects.filter(lecture=content,main_comment).count()
            # number_of_comments  = len(comments)
         
            if user.is_authenticated:
                comment_form  = CommentForm()
            else:
                comment_form = None
            
           
            context= {
                'profile':profile,
                'contents':contents,
                'content': content,
                'current_chapter':chapter,
                'next_chapter':next_chapter  ,

                'previous_chapter': previous_chapter ,
                'next_content':next_content,
                'previous_content':previous_content ,

                'comment_form': comment_form,
                'current_course':current_course,
                'lecture_title': lecture,
                'main_comment':main_comment,
                # 'number_of_replies':number_of_replies,
                # 'number_of_comments':number_of_comments
            }
            return context

      
    def get (self,request,*args,**kwargs):
            context = self.load_context()
            if context['content'].preview is False: 
                if self.request.user.is_authenticated: #check if it's an autheticated user if a member?
                    if context['profile'].is_member:
                        return render(request,'content/content_detail.html',context)
                    return render(request,'content/pay_content_detail.html',context) #return a redirect 
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
            return render(request,'content/content_detail.html',context)



    def post(self, request, *args, **kwargs):
        comment_form = self.form_class(request.POST or None)
        context = self.load_context()
        lecture = context['content']
        
        # main_comment = request.POST.get('main_comment')

        return notify_comment_or_reply_create(
            self,
            comment_form,
            main_comment=request.POST.get('main_comment'),
            lecture=lecture,
            context=context,
            redirect_link=None,
            )
    























#         if main_comment is not None:
#             main_comment = int(main_comment)

#         try:
#             main_comment_instance = Comment.objects.get(id=main_comment)
#         except Comment.DoesNotExist:
#              main_comment = None
#         else:
#              main_comment = main_comment_instance

#         if comment_form.is_valid():
#             comment_content = comment_form.cleaned_data['content']
#             new_comment = Comment.objects.create_comment(
#                  user           = request.user,
#                  content        = comment_content,
#                  path           = lecture.get_comment_path,
#                  lecture        = lecture,
#                  main_comment   = main_comment
#                 )
# #it's a reply 
#             recipient = main_comment.user
#             notify.send(
#                  sender=request.user,
#                  verb=f"{request.user.email} replyed you on {lecture}",
#                  action =new_comment,
#                  target=lecture,
#                  recipient= recipient, 
#                  )     


#         return redirect(main_comment)




   