# -*- coding: utf-8 -*
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import authenticate

from accounts.models import UserProfile
from accounts.models import Transaction

from accounts.forms import UserForm
from accounts.forms import UserProfileForm
from accounts.forms import UserEditForm

from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.http import HttpResponseRedirect

from django.db.models import Sum

from django.shortcuts import redirect

import datetime


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
	context['title'] = user.username
	# context['basket'] = Basket.objects.filter(user=user)
	# context['payments'] = Pay.objects.filter(user=user)

	base = datetime.datetime.today()
	dateList = [base + datetime.timedelta(days=x) for x in range(-7, 1)]

	days = []

	for for_date in dateList:
		total = Transaction.objects.filter(
				user=user,
				public=True,
				total__lte=0,
				created_at__year=for_date.year,
				created_at__month=for_date.month,
				created_at__day=for_date.day
		).aggregate(Sum('total'))
		if total['total__sum']:
			total = total['total__sum'] * -1
		else:
			total = 0
		days.append({'date': for_date, 'total': total})

	context['days'] = days
	context['balance'] = Transaction.objects.filter(user=user, public=True).aggregate(Sum('total'))
	context['user'] = user
	return render_to_response('accounts/accounts.html', context, context_instance=RequestContext(request))


@login_required
def edit(request):
	context = {}
	user = request.user
	if request.method == 'POST':
		AccountsUserEditForm = UserEditForm(request.POST)
		if AccountsUserEditForm.is_valid():
			form_data = AccountsUserEditForm.cleaned_data
			user.username = form_data['username']
			user.first_name = form_data['first_name']
			user.last_name = form_data['last_name']
			user.email = form_data['email']
			if form_data['password']:
				user.set_password(form_data['password'])
			user.save()

			userProfile = user.get_profile()
			userProfile.gender = form_data['gender']
			userProfile.birthday = form_data['birthday']
			userProfile.save()

			if form_data['password']:
				user = authenticate(username=form_data['username'], password=form_data['password'])
				login(request, user)
			return redirect('accounts_accounts')
	else:
		AccountsUserEditForm = UserEditForm({
				'username': user.username,
				'first_name': user.first_name,
				'last_name': user.last_name,
				'email': user.email,
				'gender': user.profile.get().gender,
				'birthday': user.profile.get().birthday
			})
	context['AccountsUserEditForm'] = AccountsUserEditForm
	context['user'] = user
	return render_to_response('accounts/edit.html', context, context_instance=RequestContext(request))
