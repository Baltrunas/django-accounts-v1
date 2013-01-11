# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# import code for encoding urls and generating md5 hashes
import urllib
import hashlib


class UserProfile(models.Model):
	user = models.ForeignKey(User, null=True, related_name='profile')
	GENDER_CHOICES = (
		(True, _('Man')),
		(False, _('Women')),
	)
	gender = models.BooleanField(_('Gender'), default=False, choices=GENDER_CHOICES)
	birthday = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def gravatar(self):
		size = 70
		url = 'http://www.gravatar.com/avatar/' + hashlib.md5(self.user.email.lower()).hexdigest() + '?'
		url += urllib.urlencode({'s': str(size)})
		return url

	class Meta:
		ordering = ['-updated_at']
		verbose_name_plural = _('UserProfile')


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
