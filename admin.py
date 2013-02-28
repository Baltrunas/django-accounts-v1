# -*- coding: utf-8 -*
from django.contrib import admin
from accounts.models import UserProfile
from accounts.models import Transaction
from accounts.models import Identity


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'gender', 'birthday')
	search_fields = ('user', 'gender', 'birthday')

admin.site.register(UserProfile, UserProfileAdmin)


class IdentityAdmin(admin.ModelAdmin):
	list_display = ['id', 'provider', 'identity']
	list_filter = ['provider']

admin.site.register(Identity, IdentityAdmin)


class TransactionAdmin(admin.ModelAdmin):
	list_display = ['user', 'transection_type', 'comment', 'total', 'public', 'created_at', 'updated_at']
	search_fields = ['user', 'transection_type', 'comment', 'total', 'public', 'created_at', 'updated_at']
	list_editable = ['public']
	list_filter = ['total', 'public']

admin.site.register(Transaction, TransactionAdmin)
