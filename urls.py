from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
	url(r'^signup/$', 'accounts.views.signup', name='accounts_signup'),
	url(r'^accounts/$', 'accounts.views.my_profile', name='accounts_accounts'),
	url(r'^edit/$', 'accounts.views.edit', name='accounts_edit'),

	url(r'loginza/$', 'accounts.views.loginza', name='accounts_loginza'),

	url(r'^login/$', 'django.contrib.auth.views.login', {"template_name": "accounts/login.html"}, name='accounts_login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='accounts_logout'),
)
