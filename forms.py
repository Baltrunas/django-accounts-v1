# -*- coding: utf-8 -*-
from django.forms.widgets import Input
from django import forms
from django.utils.translation import ugettext as _
# from accounts.models import UserProfile


class Html5EmailInput(Input):
	input_type = 'email'


class Html5URLInput(Input):
	input_type = 'url'


class DataInput(Input):
	input_type = 'date'


class LoginzaUserForm(forms.ModelForm):
	username = forms.CharField(max_length=30, label=_('Log In'))
	first_name = forms.CharField(max_length=30, required=False, label=_('First Name'))
	last_name = forms.CharField(max_length=30, required=False, label=_('Last Name'))
	email = forms.CharField(max_length=30, widget=Html5EmailInput(attrs={'placeholder': 'user@example.com', 'required': 'required'}), label=_('E-Mail'))


class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=30, label=_('Log In'))
	first_name = forms.CharField(max_length=30, required=False, label=_('First Name'))
	last_name = forms.CharField(max_length=30, required=False, label=_('Last Name'))
	email = forms.CharField(max_length=30, widget=Html5EmailInput(attrs={'placeholder': 'user@example.com', 'required': 'required'}), label=_('E-Mail'))
	password = forms.CharField(widget=forms.PasswordInput, label=_('Password'), min_length=6, max_length=30)
	password_confirmation = forms.CharField(widget=forms.PasswordInput, label=_('Password Confirmation'))

	def clean_password_confirmation(self):
		if (self.cleaned_data['password_confirmation'] != self.cleaned_data.get('password', '')):
			raise forms.ValidationError(_('Passwords do not match'))
		return self.cleaned_data['password_confirmation']


class UserProfileForm(forms.ModelForm):
	gender = forms.TypedChoiceField(
		required=False,
		choices=((False, _('Women')), (True, _('Man'))),
		widget=forms.RadioSelect,
		label=_('Genter')
	)
	birthday = forms.DateField(required=False, widget=DataInput(), label=_('Birthday'))
	# tel = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': '+996 (555) 33-88-74'}))
	# url = forms.CharField(required=False, max_length=200, widget=Html5URLInput(attrs={'placeholder' : 'http://www.glav.it/'}))


class UserEditForm(forms.Form):
	username = forms.CharField(max_length=30, label=_('Log In'))
	first_name = forms.CharField(max_length=30, required=False, label=_('First Name'))
	last_name = forms.CharField(max_length=30, required=False, label=_('Last Name'))
	email = forms.CharField(max_length=30, widget=Html5EmailInput(attrs={'placeholder': 'user@example.com', 'required': 'required'}), label=_('E-Mail'))
	old_password = forms.CharField(widget=forms.PasswordInput, required=False, label=_('Old Password'), min_length=6, max_length=30)
	password = forms.CharField(widget=forms.PasswordInput, required=False, label=_('Password'), min_length=6, max_length=30)
	password_confirmation = forms.CharField(widget=forms.PasswordInput, required=False, label=_('Password Confirmation'))

	def clean_password_confirmation(self):
		if (self.cleaned_data['password_confirmation'] != self.cleaned_data.get('password', '')):
			raise forms.ValidationError(_('Passwords do not match'))
		return self.cleaned_data['password_confirmation']

	gender = forms.TypedChoiceField(
		required=False,
		choices=((False, _('Women')), (True, _('Man'))),
		widget=forms.RadioSelect,
		label=_('Genter')
	)
	birthday = forms.DateField(required=False, widget=DataInput(), label=_('Birthday'))
