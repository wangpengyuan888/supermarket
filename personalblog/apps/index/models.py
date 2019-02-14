from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from db.base_model import BaseModel


# 个人信息表
class Aboutme(BaseModel):
    name = models.CharField(max_length=20, verbose_name='姓名')
    intro = models.TextField(verbose_name='简介')
    detail_info = RichTextUploadingField(verbose_name='详细介绍')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作者信息'
        verbose_name_plural = verbose_name


# 相册表
class Share(BaseModel):
    name = models.CharField(max_length=20, verbose_name='照片名字')
    picture = models.ImageField(upload_to='picture/%Y%m', verbose_name='个人照片')
    intro = models.TextField(verbose_name='相片简介')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '相册'
        verbose_name_plural = verbose_name


# 博客分类表
class Classify(BaseModel):
    name = models.CharField(max_length=20, verbose_name='分类名')
    click_num = models.IntegerField(default=0, verbose_name='点击量')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类名'
        verbose_name_plural = verbose_name


# 标签表
class Label(BaseModel):
    label = models.CharField(max_length=10, verbose_name='标签名')
    click_num = models.IntegerField(default=0, verbose_name='点击量')

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = '标签表'
        verbose_name_plural = verbose_name


# 作废
class Blogs(BaseModel):
    recommend_rate_choices = (
        (5, '非常推荐'),
        (4, '较推荐'),
        (3, '推荐'),
        (2, '中等'),
        (1, '不推荐')
    )
    title = models.CharField(max_length=30, verbose_name='博客标题')
    author = models.CharField(max_length=30, validators='作者名字')
    content = RichTextUploadingField(verbose_name='文章详细内容')
    recommend_rate = models.SmallIntegerField(choices=recommend_rate_choices, verbose_name='推荐指数')
    classify = models.ForeignKey(to='Classify', verbose_name='分类')
    label = models.ManyToManyField(to='Label', verbose_name='博客标签')
    click_num = models.IntegerField(verbose_name='点击量', default=0)
    like = models.IntegerField(validators='点赞数', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客表'
        verbose_name_plural = verbose_name


# 博客表
class Blogs2(BaseModel):
    recommend_rate_choices = (
        (5, '非常推荐'),
        (4, '较推荐'),
        (3, '推荐'),
        (2, '中等'),
        (1, '不推荐')
    )
    title = models.CharField(max_length=30, verbose_name='博客标题')
    author = models.CharField(max_length=30, validators='作者名字')
    content = RichTextUploadingField(verbose_name='文章详细内容')
    recommend_rate = models.SmallIntegerField(choices=recommend_rate_choices, verbose_name='推荐指数')
    classify = models.ForeignKey(to='Classify', verbose_name='分类')
    label = models.ManyToManyField(to='Label', verbose_name='博客标签')
    click_num = models.IntegerField(verbose_name='点击量', default=0)
    like = models.IntegerField(validators='点赞数', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客表'
        verbose_name_plural = verbose_name
