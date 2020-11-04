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
from course.cbvs import ScheduleDeleteView, ScoreUpdateView, RateUpdateView, StudentCourseDetailView

urlpatterns = [
    path('', to_home, name="course"),
    path('<slug:kind>/', home, name="course"),
    path('teacher/create_course', create_course, name="create_course"),
    path('teacher/view_detail/<int:course_id>', view_detail, name="view_detail"),
    path('teacher/create_schedule/<int:course_id>', create_schedule, name="create_schedule"),
    path('teacher/delete_schedule/<int:schedule_id>', delete_schedule, name="delete_schedule"),
    path('teacher/score/<int:pk>', ScoreUpdateView.as_view(), name="score"),
    path('teacher/handle_course/<int:course_id>/<int:handle_kind>', handle_course, name="handle_course"),

    path('student/view/<slug:view_kind>', view_course, name="view_course"),
    path('student/operate/<int:course_id>/<slug:operate_kind>', operate_course, name="operate_course"),

    path('student/evaluate/<int:pk>', RateUpdateView.as_view(), name="evaluate"),
    path('student/view_detail/<int:pk>', StudentCourseDetailView.as_view(), name="sview_detail"),
]
