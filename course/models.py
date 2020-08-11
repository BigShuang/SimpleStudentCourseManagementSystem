from django.db import models
import datetime
from user.models import Student, Teacher


def current_year():
    # refer: https://stackoverflow.com/questions/49051017/year-field-in-django/49051348
    return datetime.date.today().year


class Course(models.Model):
    credits = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    semesters = [
        ("Autumn", "上"),
        ("Spring", "下")
    ]
    name = models.CharField(max_length=50, verbose_name="课程名")
    introduction = models.CharField(max_length=250, verbose_name="介绍")
    credit = models.IntegerField(verbose_name="学分")
    max_number = models.IntegerField(verbose_name="课程最大人数")

    year = models.IntegerField(verbose_name="年份", default=current_year)
    semester = models.CharField(max_length=5, verbose_name="学期", choices=semesters)

    # 开始后老师无法再修改课程
    start_select = models.BooleanField(verbose_name="开始选课", default=False)
    # 结束后学生不可撤课
    end_select = models.BooleanField(verbose_name="结束选课", default=False)
    is_end = models.BooleanField(verbose_name="是否结课", default=False)

    teacher = models.ForeignKey(Teacher, verbose_name="课程教师", on_delete=models.CASCADE)


def weekday_choices():
    weekday_str = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return [(i+1, weekday_str[i]) for i in range(7)]


class Schedule(models.Model):
    weekday = models.IntegerField(choices=weekday_choices(), verbose_name="日期")
    start_time = models.TimeField(verbose_name="上课时间")
    end_time = models.TimeField(verbose_name="下课时间")
    location = models.CharField(max_length=100, verbose_name="上课地点")
    remarks = models.CharField(max_length=100, verbose_name="备注")

    start_week = models.IntegerField(verbose_name="第几周开始")
    end_week = models.IntegerField(verbose_name="第几周结束")

    intervals = [
        (1, "无间隔"),
        (2, "每隔一周上一次")
    ]
    week_interval = models.IntegerField(verbose_name="周间隔", choices=intervals, default=1)

    course = models.ForeignKey(Course, verbose_name="课程名", on_delete=models.CASCADE)


class StudentCourse(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    with_draw = models.BooleanField(default=False)
    with_draw_time = models.DateTimeField(default=None, null=True)

    scores = models.IntegerField(verbose_name="成绩", null=True)
    comments = models.CharField(max_length=250, verbose_name="老师评价", null=True)
    rating = models.IntegerField(verbose_name="学生评分", null=True)
    assessment = models.CharField(max_length=250, verbose_name="学生评价", null=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)