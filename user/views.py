# usr/bin/env python3
# -*- coding:utf-8- -*-
import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views.generic import CreateView, UpdateView

from constants import INVALID_KIND
from user.forms import StuLoginForm, TeaLoginForm, StuRegisterForm, TeaRegisterForm, StuUpdateForm
from user.models import Student, Teacher


def home(request):
    return render(request, "user/login_home.html")


# def login(request, kind)
def login(request, *args, **kwargs):
    if not kwargs or "kind" not in kwargs or kwargs["kind"] not in ["teacher", "student"]:
        return HttpResponse(INVALID_KIND)

    kind = kwargs["kind"]

    if request.method == 'POST':
        if kind == "teacher":
            form = TeaLoginForm(data=request.POST)
        else:
            form = StuLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]
            if len(uid) != 10:
                form.add_error("uid", "账号长度必须为10")
            else:
                if kind == "teacher":
                    department_no = uid[:3]
                    number = uid[3:]
                    object_set = Teacher.objects.filter(department_no=department_no, number=number)
                else:
                    grade = uid[:4]
                    number = uid[4:]
                    object_set = Student.objects.filter(grade=grade, number=number)
                if object_set.count() == 0:
                    form.add_error("uid", "该账号不存在.")
                else:
                    user = object_set[0]
                    if form.cleaned_data["password"] != user.password:
                        form.add_error("password", "密码不正确.")
                    else:
                        request.session['kind'] = kind
                        request.session['user'] = uid
                        request.session['id'] = user.id
                        # successful login
                        to_url = reverse("course", kwargs={'kind': kind})
                        return redirect(to_url)

            return render(request, 'user/login_detail.html', {'form': form, 'kind': kind})
    else:
        context = {'kind': kind}
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            if kind == "teacher":
                form = TeaLoginForm({"uid": uid, 'password': '12345678'})
            else:
                form = StuLoginForm({"uid": uid, 'password': '12345678'})
        else:
            if kind == "teacher":
                form = TeaLoginForm()
            else:
                form = StuLoginForm()
        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')

        return render(request, 'user/login_detail.html', context)


def logout(request):
    if request.session.get("kind", ""):
        del request.session["kind"]
    if request.session.get("user", ""):
        del request.session["user"]
    if request.session.get("id", ""):
        del request.session["id"]
    return redirect(reverse("login"))


def register(request, kind):
    func = None
    if kind == "student":
        func = CreateStudentView.as_view()
    elif kind == "teacher":
        func = CreateTeacherView.as_view()

    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)


class CreateStudentView(CreateView):
    model = Student
    form_class = StuRegisterForm
    # fields = "__all__"
    template_name = "user/register.html"
    success_url = "login"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = None
            return self.form_invalid(form)

    def form_valid(self, form):
        # 学生注册时选定年级自动生成学号
        grade = form.cleaned_data["grade"]
        # order_by默认升序排列，number前的负号表示降序排列
        student_set = Student.objects.filter(grade=grade).order_by("-number")
        if student_set.count() > 0:
            last_student = student_set[0]
            new_number = str(int(last_student.number) + 1)
            for i in range(6 - len(new_number)):
                new_number = "0" + new_number
        else:
            new_number = "000001"

        # Create, but don't save the new student instance.
        new_student = form.save(commit=False)
        # Modify the student
        new_student.number = new_number
        # Save the new instance.
        new_student.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_student

        uid = grade + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'student'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))


class CreateTeacherView(CreateView):
    model = Teacher
    form_class = TeaRegisterForm
    template_name = "user/register.html"
    success_url = "login"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = None
            return self.form_invalid(form)

    def form_valid(self, form):
        # 老师注册时随机生成院系号, 院系号范围为[0,300)
        department_no = random.randint(0, 300)
        # 把非三位数的院系号转换为以0填充的三位字符串，如1转换为'001'
        department_no = '{:0>3}'.format(department_no)
        teacher_set = Teacher.objects.filter(department_no=department_no).order_by("-number")
        if teacher_set.count() > 0:
            last_teacher = teacher_set[0]
            new_number = int(last_teacher.number) + 1
            new_number = '{:0>7}'.format(new_number)
        else:
            new_number = "0000001"

        # Create, but don't save the new teacher instance.
        new_teacher = form.save(commit=False)
        # Modify the teacher
        new_teacher.department_no = department_no
        new_teacher.number = new_number
        # Save the new instance.
        new_teacher.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_teacher

        uid = department_no + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'teacher'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))


def update(request, kind):
    func = None
    if kind == "student":
        func = UpdateStudentView.as_view()
    elif kind == "teacher":
        func = UpdateTeacherView.as_view()

    if func:
        pk = request.session.get("id", "")
        if pk:
            context = {
                "name": request.session.get("name", ""),
                "kind": request.session.get("kind", ""),
            }
            return func(request, pk=pk, context=context)
        else:
            return redirect(reverse("login"))
    else:
        return HttpResponse(INVALID_KIND)


class UpdateStudentView(UpdateView):
    model = Student
    form_class = StuUpdateForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "student"
        return context

    def get_success_url(self):
        return reverse("course", kwargs={"kind": "student"})


class UpdateTeacherView(UpdateView):
    model = Teacher
    form_class = TeaRegisterForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateTeacherView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "teacher"
        return context

    def get_success_url(self):
        return reverse("course", kwargs={"kind": "teacher"})
