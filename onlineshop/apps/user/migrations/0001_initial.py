# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-20 15:29
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('user_name', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('1[35678]\\d{9}', '请输入正确的手机号')], verbose_name='手机号')),
                ('pet_name', models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(3, '昵称长度最小为三')], verbose_name='昵称')),
                ('pass_word', models.CharField(max_length=32, verbose_name='密码')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别')),
                ('school', models.CharField(blank=True, max_length=30, null=True, verbose_name='学校')),
                ('native_place', models.CharField(blank=True, max_length=50, null=True, verbose_name='籍贯')),
            ],
            options={
                'verbose_name': '用户表',
                'db_table': 'userTable',
            },
        ),
    ]