from django.contrib import admin
from django.urls import path
from app.views import things_api, thing_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('things/', things_api, name='things_api'),
    path('things/<int:pk>', thing_api, name='thing_api'),
]
