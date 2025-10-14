from django.urls import path
from . import views
from django.urls.resolvers import URLPattern
from typing import List

"""
URL configuration for the members_app application.

This file connects specific URL paths to the functions (views)
that handle requests for the Member model.

Routes:
    - "": Shows the list of all members (handled by member_list view).
    - "create/": Displays a form for creating a new member (handled by member_create view).

Attributes:
    app_name (str): Namespace for reversing URLs in templates and views.
    urlpatterns (List[URLPattern]): List of all routes for this app.
"""
app_name = 'members'

urlpatterns: List[URLPattern] = [
    path('', views.member_list, name='list'),
    path('create/', views.member_create, name='create'),
]
