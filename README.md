# django-accounts
Django Accounts app with Loginza support.

# Install
* add to urls.py url(r'^accounts/', include('accounts.urls')),
* add to INSTALLED_APPS in settinhs.py 'accounts',
* add in settings.py

```
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
```
* If you want to use safe mode add in settings.py

```
ACCOUNTS_LOGINZA_WIDGET = '123'  # Where 123 your widget id
ACCOUNTS_LOGINZA_KEY = 'sekret_key'  Where 'sekret_key' your secret key
```

# Fow to use
Just use...

# Futures
* Check old pass when pass changing
* Check user name when user name changing

To analization
* https://github.com/xobb1t/django-loginza-auth
* https://github.com/vgarvardt/django-loginza
* https://github.com/omab/django-social-auth
* https://github.com/bread-and-pepper/django-userena
* https://loginza.ru/api-overview
* https://loginza.ru/signin-integration



манна - баланс
карма
	рейтиг пользователя

рейтинг =
	+ рейтинг поста * 10
	+ рейтинг комента


I thing about
* Нужно ли выделять основного OAuth провайдера?
* Дата последней синхронизации с каким либо из OAuth провайдеров?
* История заходов с логом ип провайдера и т д
* В профиле зделать добавление соц логинов
* В списке на против каждого соц логина кнопки удалить или зделать основным и синхронизировать (импортировать)
* Ник (логин) не меняется или меняется только если это возможно


# ChangeLog
## 2013.02.28
### Fix
* README.md

## 2013.02.27
### Add
* Loginza auth
* Loginza register

## 2013.01.07
### Add
* Edit account

## 2012.10.25
### Fix
* README.md

## 2012.10.25
* PEP-8
* Update README.md
