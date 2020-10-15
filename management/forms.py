from django import forms

from .models import User

class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=50, label='用户名')
    password = forms.CharField(max_length=50, label='密码')


class AddUserForm(forms.ModelForm):
    def clean_type(self):
        cleaned_data=self.cleaned_data['type']
        if cleaned_data ==0:
            raise forms.ValidationError('不能添加管理员')
        return cleaned_data
    class Meta:
        model=User
        fields=(
            'username','password','phone','email','type'
        )

class ModifySelfInfoForm(forms.Form):
    username = forms.CharField(max_length=50, label='用户名')
    phone=forms.CharField(max_length=20,label='手机号')
    email=forms.EmailField(label='邮箱')
    status=forms.ChoiceField(choices=User.STATUS_ITEMS,label='状态',)