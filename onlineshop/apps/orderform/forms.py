from django import forms

from orderform.models import UserAddress, AddressList, AddressTable, AddressTable2


class CheckAddressModelForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = ['user_name']
        # error_messages = {
        #     'user_name': {
        #         'required': '收货人必须填写',
        #         'max_length': '最大长度不能超过20'
        #
        #     },
        #     'phone': {
        #         'required': '手机号必须填写',
        #         'max_length': '最大长度不能超过11'
        #     },
        #     'hcity': {
        #         'required': '省必须填写',
        #         'max_length': '最大长度不能超过10'
        #     },
        #     'hproper': {
        #         'required': '市必须填写',
        #         'max_length': '最大长度不能超过10'
        #     },
        #     'harea': {
        #         'required': '区/县必须填写',
        #         'max_length': '最大长度不能超过10'
        #     },
        #     'detail_address': {
        #         'required': '详细地址必须填写',
        #         'max_length': '最大长度不能超过100'
        #     }
        # }


class CheckAddressModelForm2(forms.ModelForm):
    # user_name = forms.CharField(max_length=11,min_length=11)
    class Meta:
        model = AddressList
        fields = ['user_name']


class CheckAddressModelForm3(forms.ModelForm):
    class Meta:
        model = AddressTable2
        fields = ['user_name', 'phone', 'hcity', 'hproper', 'harea', 'detail_address', 'is_default']
        error_messages = {
            'user_name': {
                'required': '收货人必须填写',
                'max_length': '最大长度不能超过20'

            },
            'phone': {
                'required': '手机号必须填写',
                'max_length': '最大长度不能超过11'
            },
            'hcity': {
                'required': '省必须填写',
                'max_length': '最大长度不能超过10'
            },
            'hproper': {
                'required': '市必须填写',
                'max_length': '最大长度不能超过10'
            },
            'harea': {
                'required': '区/县必须填写',
                'max_length': '最大长度不能超过10'
            },
            'detail_address': {
                'required': '详细地址必须填写',
                'max_length': '最大长度不能超过100'
            }
        }
    def checkMax(self, request):
        user_id = request.session.get('ID')
        total = AddressTable2.objects.filter(user_id=user_id).count()
        if total >= 6:
            self.add_error('phone', '收货地址最多不能超过6个哦')
            return False
        else:
            return True
