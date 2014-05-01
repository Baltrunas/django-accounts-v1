# -*- coding: utf-8 -*
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from django.contrib.auth import login
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

# from django.core.urlresolvers import reverse
# from django.contrib.auth.views import password_reset, password_reset_confirm

from accounts.forms import SignupForm
from accounts.forms import ProfileEditForm
from accounts.models import User
from billboard.models import Ad


def signup(request):
	context = {}
	context['form'] = SignupForm(request.POST or None)

	if request.POST and context['form'].is_valid():
		new_user = context['form'].save()
		context['new_user'] = new_user
		new_user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, new_user)
		return redirect('accounts_profile', username=new_user.username)

	return render_to_response('accounts/signup.html', context, context_instance=RequestContext(request))


def profile(request, username):
	context = {}
	context['ad_list'] = Ad.objects.filter(user__username__exact=username, public=True, deleted=False)
	context['profile'] = User.objects.get(username=username)

	return render_to_response('accounts/profile.html', context, context_instance=RequestContext(request))


@login_required
def edit_profile(request):
	context = {}
	form = ProfileEditForm(request.POST or None, instance=request.user)

	if request.POST and form.is_valid():
		form.save()
		return redirect('accounts_profile', username=request.user.username)

	context['form'] = form

	return render_to_response('accounts/edit_profile.html', context, context_instance=RequestContext(request))