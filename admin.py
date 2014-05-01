# -*- coding: utf-8 -*-
from django.contrib import admin
from accounts.forms import AdminUserChangeForm, AdminUserAddForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Location
from accounts.models import User


class LocationAdmin(admin.ModelAdmin):
	list_display = ['title']

admin.site.register(Location, LocationAdmin)


class UserAdmin(BaseUserAdmin):
	form = AdminUserChangeForm
	list_display = ['username', 'email']
	add_form = AdminUserAddForm
	fieldsets = (
		(None,
			{'fields': ('username', 'password')}
		),
		(u'Персональная информация',
			{'fields': ('email', 'phone', 'url', 'user_type', 'exp', 'team_size', 'year', 'location', 'delivery', )}
		),
		(u'Разрешения',
			{'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
		),
		(u'Даты',
			{'fields': ('last_login', 'date_joined')}
		),
	)
	add_fieldsets = (
		(None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2')}),
	)

admin.site.register(User, UserAdmin)
