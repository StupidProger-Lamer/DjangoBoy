from django import forms
from django.forms import DecimalField, ModelForm
from django.forms.widgets import Select


from .models import Bb, User

class BbForm(ModelForm):
	class Meta:	
		model = Bb
		fields = ('title', 'content', 'price', 'rubric')
		labels = {'title': 'Название товара'}
		help_texts = {'rubric': 'Не забудьте указать рубрику'}
		field_classes = {'price': DecimalField}
		widgets = {'rubric': Select(attrs = {'size': 8})}

class RegisterUserForm(forms.ModelForm):
	password1 = forms.CharField(label = 'Пароль')
	password2 = forms.CharField(label = 'Повторите пароль')
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
