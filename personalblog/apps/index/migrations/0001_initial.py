# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-15 05:19
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aboutme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('head_picture', models.ImageField(upload_to='head/%Y', verbose_name='头像')),
                ('intro', models.TextField(verbose_name='简介')),
                ('detail_info', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='详细介绍')),
            ],
            options={
                'verbose_name': '作者信息',
                'verbose_name_plural': '作者信息',
            },
        ),
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('title', models.CharField(max_length=30, verbose_name='博客标题')),
                ('author', models.CharField(max_length=30, verbose_name='作者名字')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='文章详细内容')),
                ('is_top', models.BooleanField(default=False, verbose_name='是否置顶')),
                ('recommend_rate', models.SmallIntegerField(choices=[(5, '非常推荐'), (4, '较推荐'), (3, '推荐'), (2, '中等'), (1, '不推荐')], verbose_name='推荐指数')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击量')),
                ('like', models.IntegerField(default=0, verbose_name='点赞数')),
            ],
            options={
                'verbose_name': '博客表',
                'verbose_name_plural': '博客表',
            },
        ),
        migrations.CreateModel(
            name='Classify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='分类名')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击量')),
            ],
            options={
                'verbose_name': '分类名',
                'verbose_name_plural': '分类名',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('label', models.CharField(max_length=10, verbose_name='标签名')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击量')),
            ],
            options={
                'verbose_name': '标签表',
                'verbose_name_plural': '标签表',
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='照片名字')),
                ('picture', models.ImageField(upload_to='picture/%Y%m', verbose_name='个人照片')),
                ('intro', models.TextField(verbose_name='相片简介')),
            ],
            options={
                'verbose_name': '相册',
                'verbose_name_plural': '相册',
            },
        ),
        migrations.AddField(
            model_name='blogs',
            name='classify',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Classify', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='blogs',
            name='label',
            field=models.ManyToManyField(to='index.Label', verbose_name='博客标签'),
        ),
    ]
