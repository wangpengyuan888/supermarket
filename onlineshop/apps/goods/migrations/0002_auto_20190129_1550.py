# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-29 15:50
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodsspu',
            options={'verbose_name': '商品spu', 'verbose_name_plural': '商品spu'},
        ),
        migrations.AlterField(
            model_name='activityzone',
            name='is_selling',
            field=models.BooleanField(choices=[(False, '下架'), (True, '上架')], default=False, verbose_name='上否上线'),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='is_selling',
            field=models.BooleanField(choices=[(False, '下架'), (True, '上架')], default=False, verbose_name='是否上架'),
        ),
        migrations.AlterField(
            model_name='goodsspu',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='商品详情'),
        ),
    ]
