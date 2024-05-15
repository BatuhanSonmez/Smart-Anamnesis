from django.contrib import admin
from django.urls import path
from smart_anamnesis import views
from django.conf import settings

urlpatterns = [
    path('module1/', views.module1_view, name='module1'),
    path('module2/', views.module2_view, name='module2'),
    path('module3/', views.module3_view, name='module3'),
    path('', views.module1_view, name='home'),  # Default to module1 view
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)