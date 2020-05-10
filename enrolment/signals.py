import django.dispatch

payment_notification = django.dispatch.Signal(providing_args=["payment_date"])