# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-16 09:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0014_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksession',
            name='end',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='tasksession',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]