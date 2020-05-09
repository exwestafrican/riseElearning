from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404
from social.models import UserProfile


class HomeView(View):
    def get (self,request,*args,**kwargs):
        profile = None
        if request.user.is_authenticated:
            profile = get_object_or_404(UserProfile,user=request.user)

        return render(request,"home.html",{'profile': profile})


class PageNotFound(View):
    def get (self,request,*args,**kwargs):
        # profile=generate_profile(self)
        profile = None
        if request.user.is_authenticated:
            profile = get_object_or_404(UserProfile,user=request.user)
        return render(request,"page_not_found.html",{'profile': profile})