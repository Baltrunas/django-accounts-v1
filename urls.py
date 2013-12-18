from django.conf.urls import patterns
from django.conf.urls import url

from django.utils.translation import ugettext_lazy as _


urlpatterns = patterns('',
	url(r'^rating/$', 'accounts.views.rating', name='accounts_rating'),
	url(r'^signup/$', 'accounts.views.signup', name='accounts_signup'),
	url(r'^edit/$', 'accounts.views.edit', name='accounts_edit'),

	url(r'loginza/$', 'accounts.views.loginza', name='accounts_loginza'),

	url(r'^login/$', 'django.contrib.auth.views.login', {"template_name": "accounts/login.html", 'extra_context': {'title': _('Sign in')}}, name='accounts_login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='accounts_logout'),
	url(r'^(?P<username>[-\D\w/_]+)/$', 'accounts.views.profile', name='accounts_profile'),
)
