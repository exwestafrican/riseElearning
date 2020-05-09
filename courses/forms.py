from django import forms
from content.models import Contents
from .models import Course,Chapter

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = [
            'chapter_number','slug',
            'course',
            
        ]
        

class ChapterAdminForm(forms.ModelForm):
    class Meta:
        model = Chapter
        exclude = ['last_saved','slug','chapter_number']


          
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     obj = kwargs.get("instance")
    #     qs = Contents.objects.filter(chapter__isnull=True)

    #     if obj:
    #         if obj.content:
    #             this_ = Contents.objects.filter(pk=obj.content.pk)
    #             qs = (qs|this_)
    #             self.fields['content'].queryset = qs
              
    #     else:
    #         self.fields['content'].queryset = qs
         

