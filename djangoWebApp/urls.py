"""djangoWebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')), #for registration etc., it is useful to have it divided once there are more apps in the project than just one
    path('account/', include('django.contrib.auth.urls')),
    path('diaries/', include('diary.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index') #possibly make a dedicated "pages" app, once there are more apps than just the diary
]
