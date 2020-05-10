from enrolment.views import MakePayment
  


from django.urls import re_path

app_name = 'enrolment'

urlpatterns = [
    re_path(r'^$', MakePayment.as_view(), name='make_payment'),
    

    
 ]

