#coding=utf-8
from django import forms
from django.forms import ModelForm
from share.models import Theme, Code,Tag

class LoginForm(forms.Form):
    """表单登录"""
    us = forms.CharField(
        label=u'用户名',
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': u'用户名', 'required': '', 'autofocus': ''}
        ),
    )
    pwd = forms.CharField(
        label=u'密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': u'密码', 'required': ''}
        )
    )
    auto_login = forms.MultipleChoiceField(
        label=u'记住密码',
        required=False,
        widget=forms.CheckboxInput
    )



