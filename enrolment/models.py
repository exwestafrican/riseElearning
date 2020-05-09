from courses.utils import alpha_numeric_generator
from datetime import datetime,timedelta
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.contrib.auth import user_logged_in
from django.utils import timezone
from .signals import payment_notification



# Create your models here.

User = settings.AUTH_USER_MODEL

TRANSACTION_STATUS_CHOICE = [
    (1,'successful'),
    (0,'failed'),
]

TRANSACTION_CARD_TYPES = [
    ('visa','Visa'),
    ('master card','Master Card')
]


class Membership(models.Model):
    user                    = models.OneToOneField(User,on_delete=models.CASCADE)
    membership_start_date   = models.DateTimeField(default=timezone.now)
    membership_end_date     = models.DateTimeField(default=timezone.now)
    # plan_type             = models.CharField(null=True , blank=True, max_length=50)



    def __str__(self):
        return self.user.username


class TransactionModelManager(models.Manager):

    def create_new_transaction(self,user,transaction_id,amount,card_type,last_four):
        if not user:
            raise ValueError("User needed to create transaction")
        if not transaction_id:
            raise ValueError("Without a Transaction id, it's impossible to trace this payment")
        
        order_id = alpha_numeric_generator(suffix="RV",size=2)+transaction_id[-4:]
        new_transaction = self.model (
                user = user,
                transaction_id=transaction_id,
                order_id = order_id,
                amount = amount,
                card_type = card_type,
                last_four = last_four
        )
        new_transaction.save(using=self._db)
        return new_transaction        



class Transaction(models.Model):
    user                 = models.ForeignKey(User,on_delete=models.CASCADE)
    transaction_id       = models.CharField(max_length=200,unique=True,null=True ,blank=True)
    order_id             = models.CharField(max_length=200,unique=True,null=True ,blank=True)
    amount               = models.DecimalField(max_digits=10,decimal_places=2,default=00.00)
    # transaction_status   = models.CharField(max_length=100, choices=TRANSACTION_STATUS_CHOICE)
    success              = models.BooleanField(default=True)
    timestamp            = models.DateTimeField(auto_now_add=True)
    card_type            = models.CharField(max_length=300,null=True ,blank=True)
    last_four            = models.PositiveIntegerField(null=True ,blank=True)
    #reocurring boolean field

    objects              = TransactionModelManager()
   

    def __str__(self):
       return self.order_id





# class CourseLikes (models.Model):
#     user    = models.OneToOneField(User,on_delete=models.CASCADE)
#     course  = models.ForeignKey(Course,on_delete=models.CASCADE)




def payment_notification_update(sender,payment_date,*args,**kwargs):
    my_membership = sender


    if payment_date >= my_membership.membership_end_date:
       
        #payment after subscription ends
        my_membership.membership_start_date = payment_date
        my_membership.membership_end_date = payment_date + timedelta(days=30,hours=10)

       
    else:
        #payment before subscription ends
        #add 30 days to end date
        my_membership.membership_end_date = my_membership.membership_end_date + timedelta(days=30,hours=10)
      

    my_membership.save()


payment_notification.connect(payment_notification_update)