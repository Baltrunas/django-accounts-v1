# -*- coding: utf-8 -*-
from django import forms

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from billboard.models import Category


class AdminUserAddForm(UserCreationForm):
	class Meta:
		model = User
	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User._default_manager.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['duplicate_username'])


class AdminUserChangeForm(UserChangeForm):
	class Meta:
		model = User


class SignupForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'required'}, render_value=False), label=_('Password'))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'required'}, render_value=False), label=_('Password (again)'))
	username = forms.CharField(label=_('Login'), max_length=512, help_text=_("30 characters or fewer. Letters, digits and "
					  "@/./+/-/_ only."),)

	def clean_username(self):
		if User.objects.filter(username__iexact=self.cleaned_data['username']):
			raise forms.ValidationError(_("This username is already in use. Please supply a different username."))
		return self.cleaned_data['username']

	def clean_email(self):
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
		return self.cleaned_data['email']

	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_('Passwords do not match!'))
		return self.cleaned_data

	def save(self, commit=True):
		user = super(SignupForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

	class Meta:
		model = User
		exclude = ['last_login', 'last_name', 'is_staff', 'is_active', 'date_joined', 'password', 'user_permissions', 'is_superuser', 'groups']


class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = User
		exclude = ['last_login', 'username', 'last_name', 'is_staff', 'is_active', 'date_joined', 'password', 'user_permissions', 'is_superuser', 'groups']