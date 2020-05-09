from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator




class MemberRequiredMixing(object):
    def dispatch(self, request, *args, **kwargs):
        model_instance = self.get_object()
        if request.user.is_staff:
            return super(MemberRequiredMixing, self).dispatch(request, *args, **kwargs)
        if model_instance.free:
            return super(MemberRequiredMixing, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("<h1>OOPS!! Not a Free Product!! </h1>")


#use this for uploading new courses 
class StaffOnlyMixing(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
            return super(StaffOnlyMixing, self).dispatch(request, *args, **kwargs)
       

    