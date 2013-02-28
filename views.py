# -*- coding: utf-8 -*
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import authenticate

from accounts.models import Identity
from accounts.models import UserProfile
from accounts.models import Transaction

from accounts.forms import UserForm
from accounts.forms import UserProfileForm
from accounts.forms import UserEditForm

from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from django.views.decorators.csrf import csrf_exempt

import urllib2

from django.db.models import Sum

from django.shortcuts import redirect

import datetime
from hashlib import md5
from django.utils import simplejson
from django.conf import settings


def body(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	try:
		response = opener.open(url)
		html = response.read()
		return html
	except:
		return False


# Loginza
@csrf_exempt
def loginza(request):
	context = {}
	context['request'] = request

	if (request.POST):
		if 'token' in request.POST:
			token = request.POST['token']
			if hasattr(settings, 'ACCOUNTS_LOGINZA_WIDGET') and hasattr(settings, 'ACCOUNTS_LOGINZA_KEY'):
				id = settings.ACCOUNTS_LOGINZA_WIDGET = 46456
				key = settings.ACCOUNTS_LOGINZA_KEY = 'd7ce6be4148147e43d10fd5ca708e4d9'
				sig = md5(token + key).hexdigest()
				loginza_url = 'http://loginza.ru/api/authinfo?token=%s&id=%s&sig=%s' % (token, id, sig)
			else:
				loginza_url = 'http://loginza.ru/api/authinfo?token=%s' % token

			context['loginza_json'] = body(loginza_url)
			context['loginza_data'] = simplejson.loads(context['loginza_json'])

			if 'error_type' not in context['loginza_json']:
				tmp_identity = Identity.objects.filter(identity=context['loginza_data']['identity'])
				if tmp_identity:
					tmp_user = User.objects.filter(profile__identity=tmp_identity[0])
				if tmp_identity and tmp_user:
					# identity = Identity.objects.get(identity=context['loginza_data']['identity'])
					user = User.objects.get(profile__identity=tmp_identity[0])

					user.backend = 'django.contrib.auth.backends.ModelBackend'

					login(request, user)
					return redirect('accounts_accounts')

					# context['error'] = 'Log ok'
					# return render_to_response('accounts/loginza_error.html', context, context_instance=RequestContext(request))
				else:
					if not tmp_identity:
						# Создаём loginza данные
						new_identity = Identity()
						new_identity.provider = context['loginza_data']['provider']
						new_identity.identity = context['loginza_data']['identity']
						new_identity.data = context['loginza_json']
						new_identity.save()
					else:
						new_identity = tmp_identity[0]

					if request.user.is_authenticated():
						user = request.user
						if UserProfile.objects.filter(user=user):
							user_profile = user.profile
						else:
							user_profile = UserProfile(user=user)
							user_profile.save()
						context['error'] = 'Reg ok old local user'
					else:
						user = User()

						user.username = context['loginza_data']['email']
						# user.first_name = userData['first_name']
						# user.last_name = userData['last_name']
						user.email = context['loginza_data']['email']
						user.set_password('password')
						user.save()

						# Заполняем профиль
						user_profile = UserProfile(user=user)
						# user_profile.save()
						context['error'] = 'Reg ok new user'

					user.get_profile().identity.add(new_identity)
					user.get_profile().save()

					user.backend = 'django.contrib.auth.backends.ModelBackend'
					# user = authenticate(username=user.username, password='password')
					login(request, user)

					return render_to_response('accounts/loginza_error.html', context, context_instance=RequestContext(request))
			else:
				context['error'] = context['loginza_json']
				return render_to_response('accounts/loginza_error.html', context, context_instance=RequestContext(request))
		else:
			context['error'] = 'No token!'
			return render_to_response('accounts/loginza_error.html', context, context_instance=RequestContext(request))
	else:
		return redirect('accounts_login', error=_('No POST date!'))


# Sign Up
def signup(request):
	context = {}
	context['title'] = _('Register')
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
	dateList = [base + datetime.timedelta(days=x) for x in range(-14, 1)]

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
