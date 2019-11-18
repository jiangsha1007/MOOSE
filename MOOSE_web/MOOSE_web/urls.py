"""OSSlib_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from view.login import *
from view.addoss import *
from view.overview import *
from view.new import *
from view.info import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('index/', index),
    path('register/', register),
    path('addoss/', overview),
    path('addtolist/', addtolist),
    path('addtomonitor/', addtomonitor),
    path(r'overview/', overview),
    path('new/', new),
    path('commit/', commit),
    path('issue/', issue),
    path('pull/', pull),
    path('author/', author),
]
