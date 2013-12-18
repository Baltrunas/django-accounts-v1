# -*- coding: utf-8 -*
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import authenticate

from accounts.models import Identity
from accounts.models import UserProfile
from accounts.models import Transaction

from accounts.forms import LoginzaUserForm
from accounts.forms import UserForm
from accounts.forms import UserProfileForm
from accounts.forms import UserEditForm

from comments.models import ExtensiveComment

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from django.template import RequestContext
# from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from django.views.decorators.csrf import csrf_exempt

import urllib2

from django.db.models import Sum

from ratings.models import TotalRatingPlus

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


def get_or_none(model, **kwargs):
	try:
		return model.objects.get(**kwargs)
	except:
	# except model.DoesNotExist:
		return None


# Loginza
@csrf_exempt
def loginza(request):
	context = {}
	context['title'] = _('Sign in')
	if (request.POST):
		if 'token' in request.POST:
			token = request.POST['token']
			if hasattr(settings, 'ACCOUNTS_LOGINZA_WIDGET') and hasattr(settings, 'ACCOUNTS_LOGINZA_KEY'):
				id = settings.ACCOUNTS_LOGINZA_WIDGET
				key = settings.ACCOUNTS_LOGINZA_KEY
				sig = md5(token + key).hexdigest()
				loginza_url = 'http://loginza.ru/api/authinfo?token=%s&id=%s&sig=%s' % (token, id, sig)
			else:
				loginza_url = 'http://loginza.ru/api/authinfo?token=%s' % token

			context['loginza_json'] = body(loginza_url)
			context['loginza_data'] = simplejson.loads(context['loginza_json'])

			if 'error_type' not in context['loginza_json']:
				identity = get_or_none(Identity, identity=context['loginza_data']['identity'])
				if identity:
					user = get_or_none(User, identity=identity)
				if identity and user:
					# перекидывать надо не на профиль пользователя, а на пред идушию страницу
					user.backend = 'django.contrib.auth.backends.ModelBackend'
					login(request, user)
					# return redirect('accounts_accounts')
					return redirect('home')
				else:
					need_change_date = False
					if request.user.is_authenticated():
						user = request.user
						if get_or_none(UserProfile, user=user):
							user_profile = user.profile
						else:
							user_profile = UserProfile(user=user)
							user_profile.save()
					else:
						user = User()

						if 'email' in context['loginza_data']:
							user.email = context['loginza_data']['email']
						else:
							need_change_date = True

						if 'nickname' in context['loginza_data']:
							user.username = context['loginza_data']['nickname']
						elif 'email' in context['loginza_data']:
							user.username = context['loginza_data']['email'].split('@')[0]
						else:
							user.username = md5('salt_name' + str(datetime.datetime.now())).hexdigest()[:8]
							need_change_date = True

						if get_or_none(User, username=user.username):
							user.username += '_' + md5(str(datetime.datetime.now())).hexdigest()[:4]
							need_change_date = True

						if 'name' in context['loginza_data']:
							if 'first_name' in context['loginza_data']['name']:
								user.first_name = context['loginza_data']['name']['first_name']
							if 'last_name' in context['loginza_data']['name']:
								user.last_name = context['loginza_data']['name']['last_name']

						user.set_password(md5('salt' + str(datetime.datetime.now())).hexdigest()[:16])
						user.save()

						# Заполняем профиль
						user_profile = UserProfile(user=user)
						# user_profile.save()
						context['error'] = 'Reg ok new user'

					if not identity:
						# Создаём loginza данные
						identity = Identity()
						identity.user = user
						identity.provider = context['loginza_data']['provider']
						identity.identity = context['loginza_data']['identity']
						identity.data = context['loginza_json']
						identity.save()

					if need_change_date:
						user.backend = 'django.contrib.auth.backends.ModelBackend'
						login(request, user)

						loginzaUserForm = LoginzaUserForm(instance=user)
						context['loginzaUserForm'] = loginzaUserForm
						return render_to_response('accounts/loginza_register.html', context, context_instance=RequestContext(request))

					user.backend = 'django.contrib.auth.backends.ModelBackend'
					# user = authenticate(username=user.username, password='password')
					login(request, user)

					return redirect('home')

					# return render_to_response('accounts/loginza_error.html', context, context_instance=RequestContext(request))
			else:
				context['error'] = context['loginza_data']['error_message']
				return render_to_response('accounts/login.html', context, context_instance=RequestContext(request))
		else:
			context['error'] = _('No token!')
			return render_to_response('accounts/login.html', context, context_instance=RequestContext(request))
	else:
		context['error'] = _('No POST date!')
		return render_to_response('accounts/login.html', context, context_instance=RequestContext(request))


# Sign Up
def signup(request):
	context = {}
	context['title'] = _('Register')
	user = User()
	if request.user.is_authenticated():
		# return redirect('accounts_accounts')
		return redirect('home')
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
			# return redirect('accounts_accounts')
			return redirect('home')
	else:
		userForm = UserForm(instance=user)
		userProfileForm = UserProfileForm(instance=userProfile)
	context['userForm'] = userForm
	context['userProfileForm'] = userProfileForm
	return render_to_response('accounts/register.html', context, context_instance=RequestContext(request))


# Profile
@login_required
def profile(request, username):
	context = {}
	user_account = get_object_or_404(User, username=username)
	context['users_count'] = User.objects.all().count()
	# context['user_position'] = User.objects.filter(sortField__lt = myObject.sortField).count()

	context['user_position'] = User.objects.filter(profile__rating__gt=user_account.get_profile().rating).order_by('-profile__rating').count() + 1

	context['title'] = user_account.username
	context['comments'] = ExtensiveComment.objects.filter(user=user_account)[:10]
	# context['basket'] = Basket.objects.filter(user=user)
	# context['payments'] = Pay.objects.filter(user=user)

	context['user_account'] = user_account
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


@login_required
def rating(request):
	context = {}
	context['title'] = _('User ratings')
	context['users'] = User.objects.all().order_by('-profile__rating')

	for u in context['users']:
		content_type = ContentType.objects.get_for_model(u)

		rating = TotalRatingPlus.objects.filter(public=True, to_user=u).aggregate(Sum('rating'))
		karma = TotalRatingPlus.objects.filter(public=True, to_user=u, content_type=content_type, object_id=u.id).aggregate(Sum('rating'))

		userProfile = u.get_profile()

		if rating['rating__sum']:
			userProfile.rating = rating['rating__sum']
		else:
			userProfile.rating = 0

		if karma['rating__sum']:
			userProfile.karma = karma['rating__sum']
		else:
			userProfile.karma = 0

		userProfile.save()

	return render_to_response('accounts/rating.html', context, context_instance=RequestContext(request))
