# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-25 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0024_skill'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chunk',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='chunk',
            name='order',
            field=models.SmallIntegerField(default=0),
        ),
    ]
