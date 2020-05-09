from django.shortcuts import render , get_object_or_404 , redirect
from .models import Contents
from django.views.generic import ListView, DetailView,CreateView, View
from courses.models import Course,Chapter,MyCourses
from django.http import Http404
from courses.utils import get_content_or_None
from comments.models import Comment
from comments.forms import CommentForm
from notification.signals import notify
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from comments.utils import notify_comment_or_reply_create
from social.models import UserProfile

# Create your views here.

# add a member required mixing to this
class ContentsDetailView(View):
    model = Contents
    template_name= 'content/content_detail.html'
    form_class = CommentForm
  

    def load_context(self):
        # profile= generate_profile(self)
        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(UserProfile,user=self.request.user)
        user = self.request.user
       
        content_slug = self.kwargs['slug']
 
        try:
            content = Contents.objects.get_queryset().related_chapters().get(slug=content_slug)
            
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
            
            comments            = Comment.objects.all().filter(lecture=content)
            current_course      = content.course
            # replied             = Comment.objects.filter(lecture=content,main_comment=)
            number_of_comments  = len(comments)
         
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
                'comments':comments,
                'comment_form': comment_form,
                'current_course':current_course,
                'number_of_comments':number_of_comments,
                'main_page':'main_page'
            }
            return context
    
   
    def get (self,request,*args,**kwargs):
            context = self.load_context()
            if context['content'].preview is False: 

                if self.request.user.is_authenticated: #check if it's an autheticated user if a member?
                    if context['profile'].is_member:
                        return render(request,'content/content_detail.html',context)
                    return render(request,'content/pay_content_detail.html',context) #return a redirect 
           
                
                # print(request.path)
                # print('%s?next=%s' % (settings.LOGIN_URL, request.path))
                # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')

            return render(request,'content/content_detail.html',context)



    def post(self, request, *args, **kwargs):
        comment_form = self.form_class(request.POST or None)
        content_slug = self.kwargs['slug']
        lecture = Contents.objects.get(slug=content_slug)
        context = self.load_context()

        main_comment = request.POST.get('main_comment')
    
        return notify_comment_or_reply_create(
                            self,
                            comment_form,
                            main_comment,
                            lecture,
                            context,
                            redirect_link=lecture,
                            )




















# if main_comment is not None:
        #     main_comment = int(main_comment)

        # try:
        #     main_comment_instance = Comment.objects.get(id=main_comment)
        # except Comment.DoesNotExist:
        #      main_comment = None
        # else:
        #      main_comment = main_comment_instance

        # if comment_form.is_valid():
        #     comment_content = comment_form.cleaned_data['content']
        #     new_comment = Comment.objects.create_comment(
        #          user           = request.user,
        #          content        = comment_content,
        #          path           = lecture.get_comment_path,
        #          lecture        = lecture,
        #          main_comment   = main_comment
        #         )

        #     if main_comment is None:
        #         #then it's a question
        #         creator = context['current_course'].uploaded_by
                
        #         notify.send(
        #             sender=request.user, 
        #             verb=f"{request.user.email} asked a question on {lecture}",
        #             action =new_comment,
        #             target=lecture,
        #             recipient=creator, 
        #             )
                   
                
                    
        #     else:
        #         #it's a reply 
        #         # replies = Comment.objects.filter(main_comment=main_comment)
        #         # number_of_replies = len(replies)
        #         # context['number_of_replies']= number_of_replies
        #         recipient = main_comment.user
        #         notify.send(
        #          sender=request.user,
        #          verb=f"{request.user.email} replyed you on {lecture}",
        #          action =new_comment,
        #          target=lecture,
        #          recipient= recipient, 
                 
        #          ) 