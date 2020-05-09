from django.contrib import admin
from . models import Notification, TaggedItem
from .models import Notification

# Register your models here.



class NotificationAdmin(admin.ModelAdmin):
    # readonly_fields     = ['slug','views','number_of_chapters','video_count','excersise_count']
    list_display        = ['recipient','__str__']
    # list_filter         = ['level']
    search_fields       = ['recipient','sender_object']

    class meta:
        model = Notification

admin.site.register(Notification,NotificationAdmin)

admin.site.register(TaggedItem)

