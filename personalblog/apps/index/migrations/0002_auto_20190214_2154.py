# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-14 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutme',
            name='intro',
            field=models.TextField(verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='share',
            name='intro',
            field=models.TextField(verbose_name='相片简介'),
        ),
    ]