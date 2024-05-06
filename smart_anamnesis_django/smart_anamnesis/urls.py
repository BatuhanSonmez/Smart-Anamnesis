from django.urls import path
from . import views

urlpatterns = [
    path('module1/', module1_view, name='module1'),
    path('module2/', module2_view, name='module2'),
]
