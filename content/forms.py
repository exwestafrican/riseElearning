from django import forms
from .models import Contents



class ContentAdminForm(forms.ModelForm):
    class Meta:
       model     = Contents
       exclude   = ['slug','course']



#ignore
         
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     obj = kwargs.get("instance")
    #     qs = Contents.objects.filter(chapter__isnull=True)
        
    #     if obj:
    #         if obj.lecture:
    #             this_ = Contents.objects.filter(pk=obj.contents.pk)
    #             print(this_)
    #             qs = (qs|this_)
    #             self.fields['content'].queryset = qs
              
    #     else:
    #         self.fields['content'].queryset = qs




    
  
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         model_instance = kwargs.get("instance")
#         course = kwargs.get("course")
#         print(f'key word args is {kwargs}')
#         print(f'model_instance is  {model_instance}')
#         print(f'course is {course}')
      
#         if model_instance:
#             qs = course.chapter_set.all()
#             self.fields['chapter'].queryset = qs
    