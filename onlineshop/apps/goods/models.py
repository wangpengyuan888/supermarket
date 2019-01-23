from django.db import models

# Create your models here.
from db.base_model import BaseModel

is_selling = (
    (False, '下架'),
    (True, '下架')
)

# 商品分类表
class GoodsCategory(BaseModel):
    cname = models.CharField(max_length=20, verbose_name='分类名称')
    intro = models.CharField(max_length=300, blank=True, null=True, verbose_name='分类简介')
    class Meta:
        db_table = 'GoodsCategory'
        verbose_name = '商品分类管理'
        verbose_name_plural = '商品分类管理'

    def __str__(self):
        return self.cname


# 商品spu表
class GoodsSPU(BaseModel):
    spu_name = models.CharField(max_length=30, verbose_name='商品spu名称')
    content = models.TextField(verbose_name='商品详情')
    class Meta:
        db_table = 'GoodsSPU'
        verbose_name = '商品sup'

    def __str__(self):
        return self.spu_name

#商品单位表
class Unit(BaseModel):
    unit_name = models.CharField(max_length=20, verbose_name='商品单位名')
    class Meta:
        db_table = 'Unit'
        verbose_name = '商品单位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.unit_name


# 商品sku表
class GoodsSKU(BaseModel):
    good_name_sku = models.CharField(max_length=88, verbose_name='商品sku名称')
    intro = models.CharField(max_length=100, blank=True, null=True, verbose_name='商品简介')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='价格')
    unit = models.ForeignKey(to=Unit, verbose_name='单位')
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales =models.IntegerField(default=0, verbose_name='销量')
    # 默认相册中的第一张图片作为封面图片
    logo = models.ImageField(upload_to='goods/%Y%m/%d', verbose_name='封面图片')
    is_selling = models.BooleanField(choices=is_selling, default=False, verbose_name='是否上架')
    goods_category = models.ForeignKey(to=GoodsCategory, verbose_name='商品分类')
    good_spu = models.ForeignKey(to=GoodsSPU, verbose_name='商品spu')

    def __str__(self):
        return self.good_name_sku

    class Meta:
        db_table = 'GoodsSKU'
        verbose_name = '商品sku管理'
        verbose_name_plural = verbose_name

# 商品相册
class GoodsAlbum(BaseModel):
    img_url = models.ImageField(upload_to='goods_gallery/%Y%m/%d', verbose_name='相册图片地址')
    goods_sku = models.ForeignKey(to="GoodsSKU", verbose_name="商品SKU")

    class Meta:
        db_table = 'GoodsAlbum'
        verbose_name = "商品相册管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "商品相册:{}".format(self.img_url.name)


# '首页轮播'
class Banner(BaseModel):
    name = models.CharField(max_length=200, verbose_name='轮播活动名')
    good_sku = models.ForeignKey(to=GoodsSKU, verbose_name='商品sku')
    order = models.SmallIntegerField(default=0, verbose_name='排序')
    img_url = models.ImageField(upload_to='banner/%Y%m/%d', verbose_name='轮播图片地址')

    class Meta:
        db_table = 'Banner'
        verbose_name = '轮播管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# '首页活动'

class Activity(BaseModel):
    title = models.CharField(verbose_name='活动名称', max_length=150)
    img_url = models.ImageField(verbose_name='活动图片地址',
                                upload_to='activity/%Y%m/%d'
                                )
    url_site = models.URLField(verbose_name='活动的url地址', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Activity'
        verbose_name = "活动管理"
        verbose_name_plural = verbose_name


# 活动专区
class ActivityZone(BaseModel):
    title = models.CharField(verbose_name='活动专区名称', max_length=150)
    brief = models.CharField(verbose_name="活动专区的简介",
                             max_length=200,
                             null=True,
                             blank=True,
                             )
    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )
    is_selling = models.BooleanField(verbose_name="上否上线",
                                     choices=is_selling,
                                     default=False,
                                     )
    goods_sku = models.ManyToManyField(to="GoodsSKU",verbose_name="商品")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ActivityZone'
        verbose_name = "活动专区管理"
        verbose_name_plural = verbose_name




