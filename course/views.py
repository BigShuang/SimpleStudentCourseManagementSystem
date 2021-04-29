from django.http.response import HttpResponse
from django.shortcuts import render, reverse, redirect
from django.db.models import Q

from constants import INVALID_KIND, INVALID_REQUEST_METHOD, ILLEGAL_KIND
from course.forms import CourseForm, ScheduleForm
from course.models import Course, StudentCourse, Schedule
from user.util import get_user

from django.utils import timezone


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

    is_search = False
    search_key = ""
    if request.method == "POST":
        search_key = request.POST.get("search")
        if search_key:
            is_search = True

    context = {"info": info}
    q = Q(teacher=user)
    if is_search:
        q = q & Q(name__icontains=search_key)
        context["search_key"] = search_key

    context["course_list"] = Course.objects.filter(q).order_by('status')

    return render(request, 'course/teacher/home.html', context)


def student_home(request):
    return redirect(reverse("view_course", kwargs={"view_kind": "current"}))


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
            obj.status = 1
            obj.teacher = user

            obj.save()
            return redirect(reverse("course", kwargs={"kind": "teacher"}))
    elif request.method == 'GET':
        form = CourseForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    return render(request, 'course/teacher/create_course.html', {'info': info, 'form': form})


def create_schedule(request, course_id):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    course = Course.objects.get(pk=course_id)

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()

            return redirect(reverse("view_detail", kwargs={"course_id": course_id}))
    elif request.method == 'GET':
        form = ScheduleForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    return render(request, 'course/teacher/create_schedule.html', {'info': info, 'form': form, "course": course})


def delete_schedule(request, schedule_id):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    schedule = Schedule.objects.get(pk=schedule_id)

    course_id = request.GET.get("course_id") or schedule.course.id

    schedule.delete()

    return redirect(reverse("view_detail", kwargs={"course_id": course_id}))


def handle_course(request, course_id, handle_kind):
    """
    :param request:
    :param course_id:
    :param handle_kind:
            1: "开始选课",
            2: "结束选课",
            3: "结课",
            4: "给分完成"
    :return:
    """
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    course = Course.objects.get(pk=course_id)
    if course.status == handle_kind and course.status < 5:
        if course.status == 4:
            scs = StudentCourse.objects.filter(course=course)
            all_given = True
            res = ""
            for sc in scs:
                if sc.scores is None:
                    all_given = False
                    res += "<div>%s 未打分</div>" % sc.student

            if all_given:
                course.status += 1
                course.save()
                return redirect(reverse("view_detail", kwargs={"course_id": course.id}))
            else:
                return HttpResponse(res)
        else:
            course.status += 1
            course.save()

    course_list = Course.objects.filter(teacher=user)
    return render(request, 'course/teacher/home.html', {'info': info, 'course_list': course_list})


def view_detail(request, course_id):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    course = Course.objects.get(pk=course_id)
    c_stu_list = StudentCourse.objects.filter(course=course)
    sche_list = Schedule.objects.filter(course=course)

    context = {
        "info": info,
        "course": course,
        "course_students": c_stu_list,
        "schedules": sche_list
    }

    if course.status == 5:
        sorted_cs_list = sorted(c_stu_list, key=lambda cs: cs.scores)
        context["sorted_course_students"] = sorted_cs_list

    return render(request, "course/teacher/course.html", context)


def view_course(request, view_kind):
    """
    :param view_kind:
        current: 查看当前课程
        is_end: 查看结课课程
        select: 选课
        withdraw: 撤课
    """
    user = get_user(request, "student")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "student"}))

    is_search = False
    search_key = ""
    if request.method == "POST":
        search_key = request.POST.get("search")
        if search_key:
            is_search = True

    info = {
        "name": user.name,
        "kind": "student",
    }

    course_list = []

    if view_kind in ["select", "current", "withdraw", "is_end"]:
        if view_kind == "select":
            q = Q(status=2)
            if is_search:
                q = q & (Q(name__icontains=search_key) | Q(teacher__name__icontains=search_key))

            course_list = Course.objects.filter(q)

            my_course = StudentCourse.objects.filter(Q(student=user) & Q(with_draw=False))
            my_cids = [c.course.id for c in my_course]
            course_list = [c for c in course_list if c.id not in my_cids]
        else:
            q = Q(student=user) & Q(with_draw=False)
            if is_search:
                q = q & (Q(course__name__icontains=search_key) | Q(course__teacher__name__icontains=search_key))
            my_course = StudentCourse.objects.filter(q)
            if view_kind == "current":
                course_list = [c.course for c in my_course if c.course.status < 4]
            elif view_kind == "withdraw":
                course_list = [c.course for c in my_course if c.course.status == 2]
            elif view_kind == "is_end":
                course_list = [c for c in my_course if c.course.status >= 4]

    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    context = {
        'info': info,
        'view_kind': view_kind,
        'course_list': course_list
    }
    if is_search:
        context["search_key"] = search_key

    return render(request, 'course/student/home.html', context)


def operate_course(request, operate_kind, course_id):
    """
    :param operate_kind:
        current: 查看当前课程
        is_end: 查看结课课程
        select: 选课
        withdraw: 撤课
    """
    user = get_user(request, "student")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "student"}))

    if operate_kind not in ["select", "withdraw"]:
        return HttpResponse(ILLEGAL_KIND)
    elif operate_kind == "select":
        course = Course.objects.filter(pk=course_id).get()
        new_course = StudentCourse(student=user, course=course)
        new_course.save()
    elif operate_kind == "withdraw":
        q = Q(course__id=course_id) & Q(student=user) & Q(with_draw=False)
        course = StudentCourse.objects.filter(q).get()
        course.with_draw = True
        course.with_draw_time = timezone.now()
        course.save()

    return redirect(reverse("view_course", kwargs={"view_kind": operate_kind}))
