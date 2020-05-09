from django.contrib import admin
from social.models import UserProfile
# Register your models here.

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display      = ['__str__']
    # list_editable   = ['membership_start_date','membership_end_date']

    class Meta:
        model = UserProfile
    

admin.site.register(UserProfile,UserProfileAdmin)