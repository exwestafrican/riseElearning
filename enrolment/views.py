from courses.utils import alpha_numeric_generator
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction, Membership
from .signals import payment_notification


# Create your views here.

class MakePayment(LoginRequiredMixin,View):
    def get (self,request,*args,**kwargs):

        # new_transaction = Transaction.objects.create_new_transaction(
        #                 user=request.user,
        #                 transaction_id=alpha_numeric_generator('FW',5),
        #                 amount=90,
        #                 card_type='Visa',
        #                 last_four='9978'
        #                 )
        # if new_transaction.success:
        #    my_membership = Membership.objects.get(user=request.user) 
        #    payment_notification.send(
        #             sender=my_membership,
        #             payment_date= new_transaction.timestamp
        #             )
        context={}
        return render(request,'enrolment/upgrade_account.html',context)