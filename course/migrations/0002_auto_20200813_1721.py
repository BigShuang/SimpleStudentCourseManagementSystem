# Generated by Django 2.2.11 on 2020-08-13 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('Autumn', '上'), ('Spring', '下')], max_length=20, verbose_name='学期'),
        ),
    ]
