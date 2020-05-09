from django.contrib import admin
from .models import Contents


# Register your models here.



class ContentAdmin(admin.ModelAdmin):
    readonly_fields = ['last_saved','slug','course',]
    list_display     =['title','course','chapter','order']
    # exclude = ['course','chapter'] #consider making this read only

    class  meta():
         model_fields = Contents


admin.site.register(Contents,ContentAdmin)
