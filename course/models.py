from django.db import models
import datetime
from user.models import Student, Teacher
from constants import COURSE_STATUS, COURSE_OPERATION


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
    semester = models.CharField(max_length=20, verbose_name="学期", choices=semesters)

    # 未开始选课， 1
    # 开始选课，未结束选课 2
    # 结束选课， 3
    # 结课 4
    # 已打完分 5
    status = models.IntegerField(verbose_name="课程状态", default=1)

    teacher = models.ForeignKey(Teacher, verbose_name="课程教师", on_delete=models.CASCADE)

    def get_status_text(self):
        return COURSE_STATUS[self.status]

    def get_op_text(self):
        return COURSE_OPERATION[self.status]

    def get_current_count(self):
        courses = StudentCourse.objects.filter(course=self, with_draw=False)
        return len(courses)

    def get_schedules(self):
        schedules = Schedule.objects.filter(course=self)
        return schedules

    def __str__(self):
        return "%s (%s)" % (self.name, self.teacher.name)


def weekday_choices():
    weekday_str = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return [(i+1, weekday_str[i]) for i in range(7)]


class Schedule(models.Model):
    weekday = models.IntegerField(choices=weekday_choices(), verbose_name="日期")
    start_time = models.TimeField(verbose_name="上课时间")
    end_time = models.TimeField(verbose_name="下课时间")
    location = models.CharField(max_length=100, verbose_name="上课地点")
    remarks = models.CharField(max_length=100, verbose_name="备注", null=True, blank = True)

    start_week = models.IntegerField(verbose_name="第几周开始")
    end_week = models.IntegerField(verbose_name="第几周结束")

    intervals = [
        (1, "无间隔"),
        (2, "每隔一周上一次")
    ]
    week_interval = models.IntegerField(verbose_name="周间隔", choices=intervals, default=1)

    course = models.ForeignKey(Course, verbose_name="课程名", on_delete=models.CASCADE)

    def __str__(self):
        s = "第%s周-第%s周 " % (self.start_week, self.end_week)
        if self.week_interval == 2:
            s += "隔一周 "
        s += "%s %s-%s " % (self.get_weekday_display(), self.start_time.strftime("%H:%M"),
                            self.end_time.strftime("%H:%M"))
        s += "在%s" % self.location
        if self.remarks:
            s += " %s" % self.remarks
        return s


class StudentCourse(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    with_draw = models.BooleanField(default=False)
    with_draw_time = models.DateTimeField(default=None, null=True)

    scores = models.IntegerField(verbose_name="成绩", null=True)
    comments = models.CharField(max_length=250, verbose_name="老师评价", null=True)

    rates = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    rating = models.IntegerField(verbose_name="学生评分", choices=rates, null=True, help_text="5分为最满意，最低分是1分")
    assessment = models.CharField(max_length=250, verbose_name="学生评价", null=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
