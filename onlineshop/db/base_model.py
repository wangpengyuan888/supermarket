# 每个model都包含的基础model
from django.db import models

class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间",
                                       auto_now_add=True,
                                       )
    update_time = models.DateTimeField(verbose_name="更新时间",
                                       auto_now=True,
                                       )
    is_delete = models.BooleanField(verbose_name="是否删除",
                                    default=False,
                                    )

    class Meta:
        # 说明是一个抽象模型类，不会被迁移
        abstract = True
