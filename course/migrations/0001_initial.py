# Generated by Django 2.2.5 on 2020-06-29 14:27

import course.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='课程名')),
                ('introduction', models.CharField(max_length=250, verbose_name='介绍')),
                ('credit', models.IntegerField(verbose_name='学分')),
                ('max_number', models.IntegerField(verbose_name='课程最大人数')),
                ('year', models.IntegerField(default=course.models.current_year, verbose_name='年份')),
                ('semester', models.CharField(choices=[('Autumn', '上'), ('Spring', '下')], max_length=5, verbose_name='学期')),
                ('start_select', models.BooleanField(default=False, verbose_name='开始选课')),
                ('end_select', models.BooleanField(default=False, verbose_name='结束选课')),
                ('is_end', models.BooleanField(default=False, verbose_name='是否结课')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher', verbose_name='课程教师')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('with_draw', models.BooleanField(default=False)),
                ('with_draw_time', models.DateTimeField(default=None, null=True)),
                ('scores', models.IntegerField(null=True, verbose_name='成绩')),
                ('comments', models.CharField(max_length=250, null=True, verbose_name='老师评价')),
                ('rating', models.IntegerField(null=True, verbose_name='学生评分')),
                ('assessment', models.CharField(max_length=250, null=True, verbose_name='学生评价')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, '周一'), (2, '周二'), (3, '周三'), (4, '周四'), (5, '周五'), (6, '周六'), (7, '周日')], verbose_name='日期')),
                ('start_time', models.TimeField(verbose_name='上课时间')),
                ('end_time', models.TimeField(verbose_name='下课时间')),
                ('location', models.CharField(max_length=100, verbose_name='上课地点')),
                ('remarks', models.CharField(max_length=100, verbose_name='备注')),
                ('start_week', models.IntegerField(verbose_name='第几周开始')),
                ('end_week', models.IntegerField(verbose_name='第几周结束')),
                ('week_interval', models.IntegerField(choices=[(1, '无间隔'), (2, '每隔一周上一次')], default=1, verbose_name='周间隔')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='课程名')),
            ],
        ),
    ]
