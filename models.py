# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# import code for encoding urls and generating md5 hashes
import urllib
import hashlib


class Identity(models.Model):
	user = models.ForeignKey(User, null=True, related_name='identity')
	identity = models.CharField(_('identity'), max_length=255, unique=True)
	provider = models.CharField(_('provider'), max_length=255)
	data = models.TextField(_('data'))

	# objects = IdentityManager()

	def __unicode__(self):
		return self.identity

	class Meta:
		ordering = ['id']
		verbose_name = _('Identity')
		verbose_name_plural = _('Identities')


class UserProfile(models.Model):
	user = models.ForeignKey(User, null=True, related_name='profile')
	GENDER_CHOICES = (
		(True, _('Man')),
		(False, _('Women')),
	)
	gender = models.BooleanField(_('Gender'), default=False, choices=GENDER_CHOICES)
	birthday = models.DateField(blank=True, null=True)

	# identity = models.ManyToManyField(Identity, related_name='local_profile', verbose_name=_('Identity'), null=True, blank=True)
	# verified = models.BooleanField(_('active'), default=False, db_index=True)

	public = models.BooleanField(_('Public'), default=False, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# objects = UserMapManager()

	def gravatar(self):
		size = 70
		url = 'http://www.gravatar.com/avatar/' + hashlib.md5(self.user.email.lower()).hexdigest() + '?'
		url += urllib.urlencode({'s': str(size)})
		return url

	def __unicode__(self):
		return str(self.user)

	class Meta:
		ordering = ['user']
		verbose_name = _('User Profile')
		verbose_name_plural = _('User Profiles')


def user_post_save(sender, instance, **kwargs):
	(profile, new) = UserProfile.objects.get_or_create(user=instance)

# Save profile when User save!
models.signals.post_save.connect(user_post_save, sender=User)


class Transaction(models.Model):
	user = models.ForeignKey(User, related_name='transactions', verbose_name=_('User'))
	TRANSACTION_PRICE_CHOICES = (
		('servece', 'servece'),
		('product', 'product'),
		('balance', 'balance'),
		('bonus', 'bonus'),
	)
	transection_type = models.CharField(verbose_name=_('Transaction Type'), max_length=50, choices=TRANSACTION_PRICE_CHOICES)
	# зделать тип транзакции foreginkey

	comment = models.TextField(verbose_name=_('Comment'), blank=True)
	description = models.TextField(verbose_name=_('Description'), blank=True)

	# добавить отправителя платежа или получателя
	total = models.DecimalField(verbose_name=_('Total'), max_digits=10, decimal_places=4)
	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def balabce(self):
		pass

	def __unicode__(self):
		display = '#%s' % self.id
		return display

	class Meta:
		ordering = ['-updated_at']
		verbose_name = _('Transaction')
		verbose_name_plural = _('Transactions')
