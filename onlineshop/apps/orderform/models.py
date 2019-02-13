from django.db import models
from django.core.validators import RegexValidator
from db.base_model import BaseModel
from user.models import UserTable
from db.base_model import BaseModel
# 作废
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

# 作废
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

# 作废
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

# 收获地址管理
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


# 运输方式管理
class Expressage(BaseModel):
    name = models.CharField(max_length=10, verbose_name='快递名称')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='运费')

    class Meta:
        verbose_name = '快递选择'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 订单基本信息表
class Order(BaseModel):
    order_status_choices = (
        (0, '待支付'),
        (1, '待发货'),
        (2, '待收货'),
        (3, '待评价'),
        (4, '已完成'),
        (5, '退发货'),
        (6, '取消订单'),

    )
    user = models.ForeignKey(to='user.UserTable', verbose_name='用户')
    order_sn = models.CharField(max_length=64, verbose_name='订单编号')
    goods_total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='商品总金额')
    transport_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='运费')
    transport = models.CharField(max_length=50, verbose_name='运输方式')
    username = models.CharField(max_length=50, verbose_name='收货人姓名')
    phone = models.CharField(max_length=11, verbose_name='收货人电话')
    address = models.CharField(max_length=250, verbose_name='收货人地址')
    order_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='订单总金额')
    order_status = models.SmallIntegerField(choices=order_status_choices, default=0, verbose_name='订单状态')
    payment = models.ForeignKey(to="Payment", null=True, blank=True, verbose_name='支付方式')
    pay_time = models.DateTimeField(verbose_name='支付时间', null=True, blank=True)
    deliver_time = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    finish_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    def __str__(self):
        return self.order_sn
    class Meta:
        verbose_name = '订单管理'
        verbose_name_plural = verbose_name

# 订单商品表
class OrderGoods(BaseModel):
    order = models.ForeignKey(to='Order', verbose_name='订单id')
    good_sku = models.ForeignKey(to='goods.GoodsSKU', verbose_name='订单商品id')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='商品价格')
    count = models.SmallIntegerField(verbose_name='订单商品数量')
    def __str__(self):
        return '{}:{}'.format(self.order.order_sn, self.good_sku.good_name_sku)
    class Meta:
        verbose_name = '订单商品管理'
        verbose_name_plural = verbose_name


#支付方式表
class Payment(BaseModel):
    name = models.CharField(max_length=50, verbose_name='支付方式')
    brief = models.CharField(max_length=200, verbose_name='说明')
    logo = models.ImageField(upload_to='payment/%Y', verbose_name='支付logo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '支付方式管理'
        verbose_name_plural = verbose_name
