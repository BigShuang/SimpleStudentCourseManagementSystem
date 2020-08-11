# usr/bin/env python
# -*- coding:utf-8- -*-
from user.models import Student, Teacher


def get_user(request, kind):
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