# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-13 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orderform', '0004_auto_20190213_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orderform.Payment', verbose_name='支付方式'),
        ),
    ]
