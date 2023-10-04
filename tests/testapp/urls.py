"""testapp URL Configuration

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
from .models import TestModel
from .views import add_message_view
from .views import update_message_view
from .views import remove_messages_view
from .views import get_messages_view

kwargs = dict(model=TestModel)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_message/testmodel/<int:obj_id>/', add_message_view, kwargs),
    path('update_message/<msg_id>/', update_message_view),
    path('remove_messages/testmodel/<int:obj_id>/', remove_messages_view, kwargs),
    path('remove_messages/testmodel/', remove_messages_view, kwargs),
    path('remove_messages/<msg_id>/', remove_messages_view, kwargs),
    path('remove_messages/', remove_messages_view),
    path('get_messages/testmodel/<int:obj_id>/', get_messages_view, kwargs),
    path('get_messages/testmodel/', get_messages_view, kwargs),
    path('get_messages/<msg_id>/', get_messages_view),
    path('get_messages/', get_messages_view),
]
