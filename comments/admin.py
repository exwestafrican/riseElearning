from django.contrib import admin

# Register your models here.
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['slug',]
    # list_display     =['title','course','chapter','order']
    # exclude = ['course','chapter'] #consider making this read only

    class meta():
         model_fields = Comment



admin.site.register(Comment,CommentAdmin)