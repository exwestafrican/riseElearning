from django.contrib import admin
from enrolment.models import Membership,Transaction
# Register your models here.

# Register your models here.


class MembershipAdmin(admin.ModelAdmin):
    list_display      = ['__str__','membership_start_date','membership_end_date']
    # list_editable   = ['membership_start_date','membership_end_date']

    class Meta:
        model = Membership
    

admin.site.register(Membership,MembershipAdmin)

admin.site.register(Transaction)