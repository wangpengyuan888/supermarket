# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 19:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('title', models.CharField(max_length=150, verbose_name='活动名称')),
                ('img_url', models.ImageField(upload_to='activity/%Y%m/%d', verbose_name='活动图片地址')),
                ('url_site', models.URLField(verbose_name='活动的url地址')),
            ],
            options={
                'verbose_name': '活动管理',
                'verbose_name_plural': '活动管理',
                'db_table': 'Activity',
            },
        ),
        migrations.CreateModel(
            name='ActivityZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('title', models.CharField(max_length=150, verbose_name='活动专区名称')),
                ('brief', models.CharField(blank=True, max_length=200, null=True, verbose_name='活动专区的简介')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_selling', models.BooleanField(choices=[(False, '下架'), (True, '下架')], default=False, verbose_name='上否上线')),
            ],
            options={
                'verbose_name': '活动专区管理',
                'verbose_name_plural': '活动专区管理',
                'db_table': 'ActivityZone',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=200, verbose_name='轮播活动名')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('img_url', models.ImageField(upload_to='banner/%Y%m/%d', verbose_name='轮播图片地址')),
            ],
            options={
                'verbose_name': '轮播管理',
                'verbose_name_plural': '轮播管理',
                'db_table': 'Banner',
            },
        ),
        migrations.CreateModel(
            name='GoodsAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('img_url', models.ImageField(upload_to='goods_gallery/%Y%m/%d', verbose_name='相册图片地址')),
            ],
            options={
                'verbose_name': '商品相册管理',
                'verbose_name_plural': '商品相册管理',
                'db_table': 'GoodsAlbum',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('cname', models.CharField(max_length=20, verbose_name='分类名称')),
                ('intro', models.CharField(blank=True, max_length=300, null=True, verbose_name='分类简介')),
            ],
            options={
                'verbose_name': '商品分类管理',
                'verbose_name_plural': '商品分类管理',
                'db_table': 'GoodsCategory',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('good_name_sku', models.CharField(max_length=88, verbose_name='商品sku名称')),
                ('intro', models.CharField(blank=True, max_length=100, null=True, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='价格')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('logo', models.ImageField(upload_to='goods/%Y%m/%d', verbose_name='封面图片')),
                ('is_selling', models.BooleanField(choices=[(False, '下架'), (True, '下架')], default=False, verbose_name='是否上架')),
            ],
            options={
                'verbose_name': '商品sku管理',
                'verbose_name_plural': '商品sku管理',
                'db_table': 'GoodsSKU',
            },
        ),
        migrations.CreateModel(
            name='GoodsSPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('spu_name', models.CharField(max_length=30, verbose_name='商品spu名称')),
                ('content', models.TextField(verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品sup',
                'db_table': 'GoodsSPU',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('unit_name', models.CharField(max_length=20, verbose_name='商品单位名')),
            ],
            options={
                'verbose_name': '商品单位',
                'verbose_name_plural': '商品单位',
                'db_table': 'Unit',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='good_spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSPU', verbose_name='商品spu'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='goods_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='商品分类'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Unit', verbose_name='单位'),
        ),
        migrations.AddField(
            model_name='goodsalbum',
            name='goods_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSKU', verbose_name='商品SKU'),
        ),
        migrations.AddField(
            model_name='banner',
            name='good_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSKU', verbose_name='商品sku'),
        ),
        migrations.AddField(
            model_name='activityzone',
            name='goods_sku',
            field=models.ManyToManyField(to='goods.GoodsSKU', verbose_name='商品'),
        ),
    ]