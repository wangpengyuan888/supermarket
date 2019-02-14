from django.db import models


class BaseModel(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        # 说明这是一个抽象模型，不会被迁移
        abstract = True
