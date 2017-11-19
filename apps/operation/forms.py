# _*_ coding:utf-8 _*_
from django import forms
from article.models import Article

# class NewArticleForm(forms.Form):
#     title = forms.CharField(required=True)
#     content = forms.TextInput(required=True)
#
# class UploadImageForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ['image']

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['author','title','desc','detail','image']

class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','desc','detail','image']