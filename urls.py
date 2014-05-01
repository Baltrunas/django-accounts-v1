# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.conf.urls import url

from django.utils.translation import ugettext_lazy as _


urlpatterns = patterns('',
	url(r'^signup/$', 'accounts.views.signup', name='accounts_signup'),
	url(r'^login/$', 'django.contrib.auth.views.login', {"template_name": "accounts/login.html", 'extra_context': {'title': _('Sign in')}}, name='accounts_login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='accounts_logout'),
	url(r'^profile/$', 'accounts.views.edit_profile', name='accounts_edit_profile'),
	url(r'^password_change/$', 'django.contrib.auth.views.password_change',
		{'post_change_redirect' : '/accounts/password_change/done/', "template_name": "accounts/password_change.html"}, name="password_change"),
	(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {"template_name": "accounts/password_change_done.html", }),
	url(r'^(?P<username>[-\D\w/_]+)/$', 'accounts.views.profile', name='accounts_profile'),
)