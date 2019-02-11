from django.db import models
from django.core.validators import RegexValidator
from db.base_model import BaseModel
from user.models import UserTable
from db.base_model import BaseModel

class UserAddress(models.Model):
    # user = models.ForeignKey(to="user.UserTable", verbose_name='创建人')
    user_name = models.CharField(max_length=20, validators='收货人')
    # phone = models.CharField(max_length=11)
    # hcity = models.CharField(max_length=10, verbose_name='省')
    # hproper = models.CharField(max_length=10, verbose_name='市')
    # harea = models.CharField(max_length=10, verbose_name='区县')
    # detail_address = models.CharField(max_length=100, verbose_name='详细地址')
    # is_default = models.BooleanField(default=False, blank=True, verbose_name='是否设为默认')

    # class Meta:
    #     db_table = 'UserAddress'
    #     verbose_name = '收获地址管理'
    #     verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.phone


class AddressList(models.Model):
    user = models.ForeignKey(to="user.UserTable", verbose_name='创建人')
    user_name = models.CharField(max_length=20, validators='收货人')
    phone = models.CharField(max_length=11,
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', '手机格式错误')
                             ],
                             verbose_name='手机号码'
                             )
    hcity = models.CharField(max_length=10, verbose_name='省')
    hproper = models.CharField(max_length=10, verbose_name='市')
    harea = models.CharField(max_length=10, verbose_name='区县')
    detail_address = models.CharField(max_length=100, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, blank=True, verbose_name='是否设为默认')

    class Meta:
        db_table = 'UserAddress'
        verbose_name = '收获地址管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


class AddressTable(BaseModel):
    user = models.ForeignKey(to='user.UserTable', verbose_name='下单人')
    user_name = models.CharField(max_length=10, verbose_name='收货人姓名')
    phone = models.CharField(max_length=11, validators=[
        RegexValidator(r'^1[3-9]\d{9}$', '手机格式错误')
    ], verbose_name='手机号')
    hcity = models.CharField(max_length=10, verbose_name='省')
    hproper = models.CharField(max_length=10, verbose_name='市')
    harea = models.CharField(max_length=10, verbose_name='区县')
    detail_address = models.CharField(max_length=100, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, blank=True, verbose_name='是否设为默认')
    class Meta:
        db_table = 'UserAddressList'
        verbose_name = '收获地址管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


class AddressTable2(BaseModel):
    user = models.ForeignKey(to='user.UserTable', verbose_name='下单人')
    user_name = models.CharField(max_length=10, verbose_name='收货人姓名')
    phone = models.CharField(max_length=11, validators=[
        RegexValidator(r'^1[3-9]\d{9}$', '手机格式错误')
    ], verbose_name='手机号')
    hcity = models.CharField(max_length=10, verbose_name='省')
    hproper = models.CharField(max_length=10, verbose_name='市')
    harea = models.CharField(max_length=10, verbose_name='区县')
    detail_address = models.CharField(max_length=100, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, blank=True, verbose_name='是否设为默认')
    class Meta:
        db_table = 'UserAddressList2'
        verbose_name = '收获地址管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name