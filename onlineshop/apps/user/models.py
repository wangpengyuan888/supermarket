import random
import string

from django.db import models
from django.core.validators import MinLengthValidator,RegexValidator
from db.base_model import BaseModel




# 用户表模型
class UserTable(BaseModel):
    user_name = models.CharField(max_length=11, unique=True, validators=[
        RegexValidator(r'1[35678]\d{9}', '请输入正确的手机号')
    ], verbose_name='手机号')
    pet_name = models.CharField(max_length=10, blank=True, null=True, unique=True, validators=[
        MinLengthValidator(3, '昵称长度最小为三')
    ], verbose_name='昵称')
    pass_word = models.CharField(max_length=32, verbose_name='密码')
    gender_choice = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(choices=gender_choice, default=1, verbose_name='性别')
    birthday = models.DateField(verbose_name='生日', auto_now_add=True)
    school = models.CharField(max_length=50, verbose_name='学校', blank=True, null=True)
    site = models.CharField(max_length=200, verbose_name='所在地', blank=True, null=True)
    native_place = models.CharField(max_length=200, verbose_name='籍贯', blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name='手机号', blank=True, null=True, validators=[
        RegexValidator(r'1[35678]\d{9}', '请输入正确的手机号')
    ])

    class Meta:
        db_table = 'userTable'
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.user_name


# 用户头像模型
class UserIcon(models.Model):
    UserId = models.ForeignKey(to='UserTable', verbose_name='用户id')
    IconId = models.IntegerField(verbose_name='图片id')
    IconUrl = models.CharField(max_length=200, verbose_name='头像位置', blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间",
                                       auto_now_add=True,
                                       )
    is_activity = models.BooleanField(verbose_name="是否使用",
                                    default=True,
                                    )

    class Meta:
        db_table = 'UerIcon'
        verbose_name = '用户头像'
        verbose_name_plural = '用户头像'

    def __str__(self):
        return self.IconId






