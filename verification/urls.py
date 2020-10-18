from django.urls import path

from .views import writeoff

urlpatterns=[
    path('writeoff/',writeoff)
]