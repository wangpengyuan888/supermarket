from django.contrib import admin

# Register your models here.
from goods.models import GoodsSKU, Banner, Activity, GoodsCategory, Unit, GoodsSPU, GoodsAlbum

@admin.register(GoodsSPU)
class GoodSPUAdmin(admin.ModelAdmin):
    # 每页显示的条数
    list_per_page = 2
    # 自定义显示列
    list_display = ['spu_name']
    actions_on_bottom = True
    actions_on_top = False
    # 编辑时可以操作那些字段
    fields = ['spu_name']
    search_fields = ['spu_name']

admin.site.register(GoodsCategory)
admin.site.register(Unit)
# admin.site.register(GoodsSPU)

admin.site.register(GoodsAlbum)
admin.site.register(GoodsSKU)


# 首页管理
admin.site.register(Banner)
admin.site.register(Activity)