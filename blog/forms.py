#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-30,11:20"

from django.forms import Form,fields,widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


from blog import models
from blog.blugins.xss_blugin import filter_xss


class RegisterForm(Form):
    email = fields.CharField(
        required=True,
        error_messages={"required":"邮箱不能为空"},
        widget=widgets.EmailInput(attrs={"placeholder":"需要通过邮箱激活账户","class":"form-control",}),
        validators=[RegexValidator("[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?","请输入正确的邮箱格式")]
    )
    telephone = fields.CharField(
        required=True,
        error_messages={"required": "手机号不能为空"},
        widget=widgets.EmailInput(attrs={"placeholder": "需要通过手机号激活账户", "class": "form-control"}),
        validators=[RegexValidator(
            "^1(3|4|5|7|8)\d{9}$","手机号码有误")]
    )
    username = fields.CharField(
        required=True,
        min_length=4,
        error_messages={
            "required":"用户名不能为空",
            "min_length":"用户名不能少于4个字符",
        },
        widget=widgets.TextInput(attrs={"placeholder":"登录用户名，不少于4个字符","class":"form-control"})
    )
    nick_name = fields.CharField(
        required=True,
        min_length=2,
        error_messages={
            "required": "昵称不能为空",
            "min_length": "昵称不能少于2个字符",
        },
        widget=widgets.TextInput(attrs={"placeholder": "昵称，不少于2个字符", "class": "form-control"})
    )
    password = fields.CharField(
        required=True,
        min_length=8,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码不能少于8个字符",
        },
        widget=widgets.PasswordInput(attrs={"placeholder": "至少8位，且必须包含字母，数字，特殊字符", "class": "form-control"}),
        validators=[RegexValidator("^(?![a-zA-Z0-9]+$)(?![^a-zA-Z/D]+$)(?![^0-9/D]+$).{10,20}$","密码必须包含字母，数字，特殊符号")]
    )
    repeat_password = fields.CharField(
        required=True,
        error_messages={
            "required": "密码不能为空",
        },
        widget=widgets.PasswordInput(
            attrs={"placeholder": "请再次输入密码", "class": "form-control"}),
    )
    def clean_username(self):
        username = models.UserInfo.objects.filter(username=self.cleaned_data.get("username"))
        if not username:
            return self.cleaned_data.get("username")
        else:
            raise ValidationError("用户名已存在")
    def clean_email(self):
        email = models.UserInfo.objects.filter(email = self.cleaned_data.get("email"))
        if not email:
            return self.cleaned_data.get("email")
        else:
            raise ValidationError("邮箱已注册")
    def clean(self):
        password = self.cleaned_data.get("password")
        repeat_password = self.cleaned_data.get("repeat_password")
        if password == repeat_password:
            return self.cleaned_data
        else:
            raise ValidationError("两次输入的密码不一致")


class ArticleForm(Form):
    title = fields.CharField(widget = widgets.TextInput(attrs = {"class":"form-control"}),error_messages = {"required":"标题不能为空"},max_length = 20)
    content = fields.CharField(widget = widgets.Textarea(attrs = {"class":"form-control"}),error_messages = {"required":"内容不能为空"})

    def clean_content(self):
        html_str = self.cleaned_data.get("content")
        clean_data = filter_xss(html_str)
        self.cleaned_data["content"] = clean_data
        return self.cleaned_data["content"]