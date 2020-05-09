import django.dispatch

notify = django.dispatch.Signal(providing_args=["verb","action","target","recipient","affected_users"])



