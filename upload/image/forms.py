#-*- coding:utf-8 -*-

from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField(label="image")

