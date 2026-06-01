from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(
        label='姓名',
        required=True,
        min_length=3,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required':'用户名不能为空',
            'min_length':'长度不小于3个字符',
            'max_length':'长度不能超过10个字符',
        }
    )
    email = forms.CharField(
        label='邮箱',
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required':'邮箱不能为空',
            'max_length':'长度不能超过50个字符',
        }
    )