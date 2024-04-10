from django import forms
from .models import MarkList, Theme, User


class ArticleForm(forms.Form):
    author = forms.CharField(max_length=256, label='Автор')
    title = forms.CharField(max_length=256, label='Название')
    link = forms.CharField(max_length=1024, label='Статья', widget=forms.Textarea)
    mark_list = forms.ChoiceField(choices=[], label='Тип оценивания', widget=forms.Select)
    theme = forms.ChoiceField(choices=[], label='Тематика', widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mark_list'].choices = [obj.title for obj in MarkList.objects.all()]
        self.fields['theme'].choices = [obj.title for obj in Theme.objects.all()]

class NewUserForm(forms.Form):
    first_name = forms.CharField(max_length=256, label='Имя')
    second_name = forms.CharField(max_length=256, label='Фамилия')
    username = forms.CharField(max_length=256, label='Логин')
    password = forms.CharField(max_length=256, label='Пароль')
    role = forms.ChoiceField(choices=User.USER_ROLE_CHOISES, label='Роль', widget=forms.Select)

class ChangeUserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=256, label='Имя')
    second_name = forms.CharField(max_length=256, label='Фамилия')
    password = forms.CharField(required=False, max_length=256, label='Пароль')
    birthday = forms.DateField(label='Дата рожждения', widget=forms.DateInput(attrs={'type': 'date'}))
    about = forms.CharField(required=False, max_length=1024, label='Персональная информация', widget=forms.Textarea)
