# usr/bin/env python
# -*- coding:utf-8- -*-
from django.http.response import HttpResponse
from django.shortcuts import reverse, redirect

from constants import *
from user.models import Student, Teacher


def check_login(func):
    # the func method must have the second parameter kind.
    def _check(*args, **kwargs):
        request = args[1]
        cookie_kind = request.session.get('kind', '')
        if cookie_kind not in ["student", "teacher"]:
            # Not logged in
            to_url = reverse("login")
            return redirect(to_url)
        elif len(args) >= 2:
            # the second parameter must be kind
            kind = args[1]
            if kind == cookie_kind:
                return func(*args, **kwargs)
            else:
                return HttpResponse(ILLEGAL_KIND)
        return HttpResponse(INVALID_URL)

    return _check


def get_user(request, kind):
    """

    :param request:
    :param kind: teacher or student
    :return: return Teacher instance or Student instance
    """
    if request.session.get('kind', '') != kind or kind not in ["student", "teacher"]:
        return None

    if len(request.session.get('user', '')) != 10:
        return None

    uid = request.session.get('user')
    if kind == "student":
        # 找到对应学生
        grade = uid[:4]
        number = uid[4:]
        student_set = Student.objects.filter(grade=grade, number=number)
        if student_set.count() == 0:
            return None
        return student_set[0]
    else:
        # 找到对应老师
        department_no = uid[:3]
        number = uid[3:]
        teacher_set = Teacher.objects.filter(department_no=department_no, number=number)
        if teacher_set.count() == 0:
            return None
        return teacher_set[0]


