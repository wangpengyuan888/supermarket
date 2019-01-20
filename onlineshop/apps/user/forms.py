from django import forms

from user.helper import set_pwd
from user.models import UserTable


class RegisterModelForm(forms.ModelForm):
    pass_word = forms.CharField(min_length=6, max_length=16, error_messages={
        'required': '密码必须填写',
        'min_length': '密码长度最少6',
        'max_length': '密码长度最大16'
    })
    re_pass_word = forms.CharField(min_length=6, max_length=16, error_messages={
        'required': '确认密码必须填写',
        'min_length': '确认密码长度最少6',
        'max_length': '确认密码长度最大16'
    })

    class Meta:
        model = UserTable
        fields = ['user_name']

        error_messages = {

            'user_name': {
                'required': '用户名必须填写',
                'max_length': '最大长度不能超过11',
            }
        }

    # 验证用户名是否已存在
    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        flag = UserTable.objects.filter(user_name=user_name).exists()
        if flag:
            raise forms.ValidationError('用户名已存在')
        else:
            return user_name


    # 验证两次密码是否一致
    def clean(self):
        pass_word = self.cleaned_data.get('pass_word')
        re_pass_word = self.cleaned_data.get('re_pass_word')
        if pass_word and re_pass_word and pass_word != re_pass_word:
            raise forms.ValidationError({'re_pass_word': '两次密码不一致'})
        else:
            return self.cleaned_data


class LoginModelForm(forms.ModelForm):
    pass_word = forms.CharField(min_length=6, max_length=16, error_messages={
        'required': '密码必须填写',
        'min_length': '密码长度最少6',
        'max_length': '密码长度最大16'
    })

    class Meta:
        model = UserTable
        fields = ['user_name']
        error_messages = {
            'user_name': {
                'required': '用户名必须填写',
                'max_length': '最大长度不能超过11'
            }
        }

    # 判断用户名和密码是否正确
    def clean(self):
        # user_name = self.cleaned_data.get('user_name')
        # # 查询用户名
        # user_info = UserTable.objects.filter(user_name=user_name)
        # if user_name.exists():
        #     # 用户名存在, 验证密码
        #     pass_word = set_pwd(self.cleaned_data.get('pass_word'))
        #     if pass_word == user_info.pass_word:
        #
        #
        # else:
        #     # 用户名不存在
        #      raise forms.ValidationError({'pass_word': '用户名或密码错误'})

        # 验证用户名
        user_name = self.cleaned_data.get('user_name')
        # 查询数据库
        try:
            user = UserTable.objects.get(user_name=user_name)
        except UserTable.DoesNotExist:
            raise forms.ValidationError({'user_name': '用户名错误'})

        # 验证密码
        pass_word = self.cleaned_data.get('pass_word', '')
        if user.pass_word != set_pwd(pass_word):
            raise forms.ValidationError({'pass_word': '密码错误'})

        # 返回所有清洗后的数据
        self.cleaned_data['user'] = user
        return self.cleaned_data