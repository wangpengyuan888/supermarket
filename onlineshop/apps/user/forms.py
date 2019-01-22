from django import forms
from django_redis import get_redis_connection

from user.helper import set_pwd
from user.models import UserTable

# 注册表单数据验证
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

    captcha = forms.CharField(max_length=6, error_messages={
        'required': '验证码必须填写'
    })

    agree = forms.BooleanField(error_messages={
        'required': '必须同意协议'
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

        try:
            # 验证验证码是否正确
            captcha = self.cleaned_data.get('captcha')
            user_name = self.cleaned_data.get('user_name', '')
            # 获取redis中的
            r = get_redis_connection()
            random_code = r.get(user_name)  # 二进制, 转码
            random_code = random_code.decode('utf-8')
            # 比对
            if captcha and captcha != random_code:
                raise forms.ValidationError({"captcha": "验证码输入错误!"})
        except:
            raise forms.ValidationError({"captcha": "验证码输入错误!"})

        # 返回清洗后的所有数据
        return self.cleaned_data

# 登陆表单验证
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


# 修改个人资料表单验证
class AlterInfoModelForm(forms.ModelForm):
    class Meta:
        model = UserTable
        fields = ['pet_name', 'school', 'site', 'native_place', 'phone', 'gender']
        error_messages = {
            'pet_name': {
                'required': '昵称必须填写',
                'max_length': '昵称最大长度为10',
                'min_length': '昵称最小长度为3'
            },
            'school': {
                'max_length': '最大长度为50'
            },
            'site': {
                'max_length': '最大长度为200'
            },
            'native_place': {
                'max_length': '最大长度为200'
            },
            'phone': {
                'max_length': '最大长度为11'
            }
        }


# 忘记密码表单验证
class AlterPassWordModelForm(forms.ModelForm):
    pass_word = forms.CharField(min_length=6, max_length=16, error_messages={
        'required': '新密码必须填写',
        'min_length': '新密码长度最少6',
        'max_length': '新密码长度最大16'
    })
    re_pass_word = forms.CharField(min_length=6, max_length=16, error_messages={
        'required': '确认新密码必须填写',
        'min_length': '确认新密码长度最少6',
        'max_length': '确认新密码长度最大16'
    })
    class Meta:
        model = UserTable
        fields = ['user_name']
        error_messages = {
            'user_name': {
                'required': '手机号必须填写',
                'max_length': '手机号最大长度为11位'
            }
        }

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        flag = UserTable.objects.filter(user_name=user_name)
        if flag:
            return user_name
        else:
            raise forms.ValidationError('改手机号未注册')


    def clean(self):
        pass_word = self.cleaned_data.get('pass_word')
        re_pass_word = self.cleaned_data.get('re_pass_word')
        if pass_word and re_pass_word and pass_word != re_pass_word:
            raise forms.ValidationError({'re_pass_word': '两次密码不一致'})
        else:
            try:
                user = UserTable.objects.filter(user_name=self.cleaned_data.get('user_name')).get(pass_word=set_pwd(pass_word))
                raise forms.ValidationError({'re_pass_word': '新老密码不能一致'})
            except UserTable.DoesNotExist:
                return self.cleaned_data


#修改密码表单验证
class PassWordForm(forms.Form):
    pass_word = forms.CharField(min_length=6, max_length=16, error_messages={
        'required': '旧密码必须填写',
        'min_length': '旧密码长度最少6',
        'max_length': '旧密码长度最大16'
    })
    new_pass_word = forms.CharField(min_length=6, max_length=16, error_messages={
        'required': '新密码必须填写',
        'min_length': '新密码长度最少6',
        'max_length': '新密码长度最大16'
    })
    re_new_pass_word = forms.CharField(min_length=6, max_length=16, error_messages={
        'required': '确认新密码必须填写',
        'min_length': '确认新密码长度最少6',
        'max_length': '确认新密码长度最大16'
    })

    # 判断两次新密码是否一致
    def clean(self):
        new_pass_word = self.cleaned_data.get('new_pass_word')
        re_new_pass_word = self.cleaned_data.get('re_new_pass_word')
        if new_pass_word and re_new_pass_word and new_pass_word != re_new_pass_word:
            raise forms.ValidationError({'re_pass_word': '两次密码不一致'})
        else:
            return self.cleaned_data

    # 判断旧密码是否正确
    def checkPassword(self, request):
        pass_word = set_pwd(self.cleaned_data.get('pass_word'))
        user_id = request.session.get('ID')
        user_info = UserTable.objects.get(pk=user_id)
        if user_info.pass_word == pass_word:
            return True
        else:
            self.add_error('pass_word', '旧密码错误')
            return False




