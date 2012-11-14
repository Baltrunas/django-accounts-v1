# -*- coding: utf-8 -*
from django.contrib import admin
from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'gender', 'birthday')
	search_fields = ('user', 'gender', 'birthday')

admin.site.register(UserProfile, UserProfileAdmin)
