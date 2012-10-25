from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
	url(r'^signup/$', 'profile.views.signup', name='signup'),
	url(r'^profile/$', 'profile.views.my_profile', name='profile'),
	url(r'^login/$', 'django.contrib.auth.views.login', {"template_name": "profile/login.html"}, name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
