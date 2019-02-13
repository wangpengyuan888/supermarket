from django.contrib import admin

# Register your models here.
from orderform.models import Expressage, Payment


@admin.register(Expressage)
class ExpressageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Payment)