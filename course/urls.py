"""scss URL Configuration

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
from django.urls import path, include
from course.views import *


urlpatterns = [
    path('', to_home, name="course"),
    path('<slug:kind>/', home, name="course"),
    path('teacher/create_course', create_course, name="create_course"),
    path('teacher/view_detail/<int:course_id>', view_detail, name="view_detail"),
    path('student/view/<slug:view_kind>', view_course, name="view_course"),
    path('student/operate/<int:course_id>/<slug:operate_kind>', operate_course, name="operate_course"),
    path('teacher/handle_course/<int:course_id>/<slug:handle_kind>', handle_course, name="handle_course"),
]
