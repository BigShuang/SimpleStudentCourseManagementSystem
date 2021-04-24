# usr/bin/env python3
# -*- coding:utf-8- -*-
from django.db import models


class Student(models.Model):
    gender = [
        ("m", "男"),
        ("f", "女")
    ]

    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=gender, default='m', verbose_name="性别")
    birthday = models.DateField(verbose_name="生日")
    email = models.EmailField(verbose_name="邮箱")
    info = models.CharField(max_length=255, verbose_name="个人简介", help_text="一句话介绍自己，不要超过250字")

    grade = models.CharField(max_length=4, verbose_name="年级")
    number = models.CharField(max_length=6, verbose_name="年级子学号")
    password = models.CharField(max_length=30, verbose_name="密码")

    class Meta:
        constraints = [
            # 复合主键：保证 grade和number组合的student_id唯一
            models.UniqueConstraint(fields=['grade', 'number'], name='student_id'),
        ]

    def get_id(self):
        return self.grade + self.number

    def __str__(self):
        return "%s (%s)" % (self.grade + self.number, self.name)


class Teacher(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女")
    ]

    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    birthday = models.DateField(verbose_name="生日")
    email = models.EmailField(verbose_name="邮箱")
    info = models.CharField(max_length=255, verbose_name="教师简介", help_text="不要超过250字")

    department_no = models.CharField(max_length=3, verbose_name="院系号")
    number = models.CharField(max_length=7, verbose_name="院内编号")
    password = models.CharField(max_length=30, verbose_name="密码")

    class Meta:
        constraints = [
            # 复合主键：保证 department_no 和number组合的 teacher_id 唯一
            models.UniqueConstraint(fields=['department_no', 'number'], name='teacher_id'),
        ]



