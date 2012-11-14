# -*- coding: utf-8 -*
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import authenticate

from accounts.models import UserProfile

from accounts.forms import UserForm
from accounts.forms import UserProfileForm

from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.http import HttpResponseRedirect

from django.shortcuts import redirect


# Sign Up
def signup(request):
	context = {}
	user = User()
	if request.user.is_authenticated():
		return redirect('accounts_accounts')
	userProfile = UserProfile()
	if request.method == 'POST':
		userForm = UserForm(request.POST, instance=user)
		userProfileForm = UserProfileForm(request.POST, instance=userProfile)
		if userForm.is_valid() and userProfileForm.is_valid():
			userData = userForm.cleaned_data
			user.username = userData['username']
			user.first_name = userData['first_name']
			user.last_name = userData['last_name']
			user.email = userData['email']
			user.set_password(userData['password'])
			user.save()

			userProfile = user.get_profile()
			userProfileData = userProfileForm.cleaned_data
			userProfile.gender = userProfileData['gender']
			userProfile.birthday = userProfileData['birthday']
			userProfile.save()

			user = authenticate(username=userData['username'], password=userData['password'])
			login(request, user)
			return redirect('accounts_accounts')
	else:
		userForm = UserForm(instance=user)
		userProfileForm = UserProfileForm(instance=userProfile)
	context['userForm'] = userForm
	context['userProfileForm'] = userProfileForm
	return render_to_response('accounts/register.html', context, context_instance=RequestContext(request))


# Profile
@login_required
def my_profile(request):
	context = {}
	user = request.user
	# context['order'] = Order.objects.filter(user=user)
	# context['basket'] = Basket.objects.filter(user=user)
	# context['payments'] = Pay.objects.filter(user=user)

	summ = 0
	# for i in context['basket']:
		# summ += i.total_price
	context['basket_summ'] = summ
	context['user'] = user
	return render_to_response('accounts/accounts.html', context, context_instance=RequestContext(request))
