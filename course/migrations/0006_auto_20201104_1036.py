# Generated by Django 2.2.11 on 2020-11-04 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20201021_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourse',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='学生评分'),
        ),
    ]
