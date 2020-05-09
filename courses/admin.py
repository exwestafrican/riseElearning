from django.contrib import admin
from .models import  Course ,Chapter,MyCourses
from .forms import ChapterAdminForm
from content.forms import ContentAdminForm
from content.models import Contents
from django.contrib.contenttypes.admin import (
    GenericTabularInline,
    GenericStackedInline ,
     GenericInlineModelAdmin )

from notification.models import TaggedItem
# Register your models here.


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 1


class ContentInline(admin.TabularInline):
    model = Contents
    form = ContentAdminForm
    extra = 0


class ChapterAdmin(admin.ModelAdmin):
    inlines         = [ContentInline,TaggedItemInline]
    list_filter     =['course','chapter_number']
    list_display    =['chapter_name','course','chapter','order']
    readonly_fields =['chapter_number','slug']
    list_editable   = ['order']
   

    class meta:
        model = Chapter

class ChapterInline(admin.TabularInline):
    
    model = Chapter
    form = ChapterAdminForm
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines             = [ChapterInline]
    readonly_fields     = ['slug','views','number_of_chapters','video_count','excersise_count']
    list_display        = ['title','level',]
    list_filter         = ['level']
    search_fields       = ['title']

    class meta:
        model = Course


    
admin.site.register(Course,CourseAdmin)

admin.site.register(Chapter,ChapterAdmin)



admin.site.register((MyCourses))