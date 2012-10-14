# -*- coding: utf-8 -*
from django.contrib import admin
from profile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'birthday')
	search_fields = ('user', 'birthday')

admin.site.register(UserProfile, UserProfileAdmin)
