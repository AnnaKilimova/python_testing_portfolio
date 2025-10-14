from django.urls import path
from . import views
from django.urls.resolvers import URLPattern
from typing import List

"""
URL configuration for the courses_app application.

This file connects specific URL paths to the functions (views)
that handle requests for the Course model.

Routes:
    - "": Shows the list of all courses (handled by course_list view).
    - "create/": Displays a form for creating a new course (handled by course_create view).

Attributes:
    app_name (str): Namespace for reversing URLs in templates and views.
    urlpatterns (List[URLPattern]): List of all routes for this app.
"""
app_name = 'courses'

urlpatterns: List[URLPattern] = [
    path('', views.course_list, name='list'),
    path('create/', views.course_create, name='create'),

]
