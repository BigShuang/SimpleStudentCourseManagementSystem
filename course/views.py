from django.http.response import HttpResponse
from django.shortcuts import render, reverse, redirect

from constants import INVALID_KIND, INVALID_REQUEST_METHOD
from course.forms import CourseForm
from course.models import Course
from user.util import get_user


def to_home(request):
    kind = request.session.get('kind', '')
    return redirect(reverse("course", kwargs={"kind": kind}))


def home(request, kind):
    if kind == "teacher":
        return teacher_home(request)
    elif kind == "student":
        return student_home(request)
    return HttpResponse(INVALID_KIND)


def teacher_home(request):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    course_list = Course.objects.filter(teacher=user)

    return render(request, 'course/teacher/home.html', {'info': info, 'course_list': course_list})


def student_home(request):
    user = get_user(request, "student")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "student"}))

    info = {
        "name": user.name,
        "kind": "student",
    }

    return render(request, 'course/student/home.html', {'info': info})


def create_course(request):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.start_select = False
            obj.end_select = False
            obj.is_end = False
            obj.teacher = user

            obj.save()
            return redirect(reverse("course", kwargs={"kind": "teacher"}))
    elif request.method == 'GET':
        form = CourseForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    return render(request, 'course/teacher/create_course.html', {'info': info, 'form': form})