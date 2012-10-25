# -*- coding: utf-8 -*-
from django.forms.widgets import Input
from django import forms

from django.utils.translation import ugettext as _


class Html5EmailInput(Input):
	input_type = 'email'


class Html5URLInput(Input):
	input_type = 'url'


class DataInput(Input):
	input_type = 'date'


class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=30, label=_('Log In'))
	firstname = forms.CharField(max_length=30, required=False, label='Имя')
	lastname = forms.CharField(max_length=30, required=False, label='Фамилия')
	email = forms.CharField(max_length=30, widget=Html5EmailInput(attrs={'placeholder': 'user@example.com', 'required': 'required'}), label='E-Mail')
	pass1 = forms.CharField(widget=forms.PasswordInput, label='Пароль', min_length=6, max_length=30)
	pass2 = forms.CharField(widget=forms.PasswordInput, label='Повтор пароля')

	def clean_pass2(self):
		if (self.cleaned_data["pass2"] != self.cleaned_data.get("pass1", "")):
			raise forms.ValidationError("Пароли не совпадают")
		return self.cleaned_data["pass2"]


class UserProfileForm(forms.ModelForm):
	birthday = forms.DateField(required=False, widget=DataInput(), label='Дата рождения')

# class ContactForm(forms.Form):
	# name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required':'required', 'placeholder' : 'Ваше Имя'}))
	# tel = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': '+996 (555) 33-88-74'}))
	# email = forms.EmailField(max_length=200, widget=Html5EmailInput(attrs={'placeholder' : 'manager@glavit.com', 'required': 'required'}))
	# url = forms.CharField(required=False, max_length=200, widget=Html5URLInput(attrs={'placeholder' : 'http://www.glavit.com/'}))
	# msg = forms.CharField(widget=forms.Textarea(attrs={'required':'required'}))
