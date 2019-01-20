from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.

class UserTable(models.Model):
    user_name = models.CharField(max_length=20, validators=[
        MinLengthValidator(4, '用户名至少4位')
    ])
    pass_word = models.CharField(max_length=32)
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'userTable'

    def __str__(self):
        return self.user_name
