# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-09 00:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190124_0026'),
        ('orderform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressTable2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('user_name', models.CharField(max_length=10, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}$', '手机格式错误')], verbose_name='手机号')),
                ('hcity', models.CharField(max_length=10, verbose_name='省')),
                ('hproper', models.CharField(max_length=10, verbose_name='市')),
                ('harea', models.CharField(max_length=10, verbose_name='区县')),
                ('detail_address', models.CharField(max_length=100, verbose_name='详细地址')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否设为默认')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserTable', verbose_name='下单人')),
            ],
            options={
                'verbose_name': '收获地址管理',
                'verbose_name_plural': '收获地址管理',
                'db_table': 'UserAddressList2',
            },
        ),
    ]
