from django.contrib import admin

# Register your models here.
from goods.models import GoodsSKU, Banner, Activity, GoodsCategory, Unit, GoodsSPU

admin.site.register(GoodsCategory)
admin.site.register(Unit)
admin.site.register(GoodsSPU)


admin.site.register(GoodsSKU)


# 首页管理
admin.site.register(Banner)
admin.site.register(Activity)