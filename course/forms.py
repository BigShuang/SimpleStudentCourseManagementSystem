# usr/bin/env python
# -*- coding:utf-8- -*-
from django import forms
from .models import Course


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ['start_select', 'end_select', 'is_end','teacher']
