# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
	user = models.ForeignKey(User, null=True)
	GENDER_CHOICES = (
		(True, _('Man')),
		(False, _('Women')),
	)
	gender = models.BooleanField(_('Gender'), default=False, choices=GENDER_CHOICES)
	birthday = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at']
		verbose_name_plural = _('UserProfile')


def user_post_save(sender, instance, **kwargs):
	(profile, new) = UserProfile.objects.get_or_create(user=instance)

# Save profile when User save!
models.signals.post_save.connect(user_post_save, sender=User)

# class Transactions( models.Model ):
	# user = models.ForeignKey(User, null = True)
	# PRICE_CHOICES = (
		# ('servece', 'servece'),
		# ('product', 'product'),
		# ('balance', 'balance'),
	# )
	# price = models.CharField(max_length=30, choices=PRICE_CHOICES)
	# id = models.IntegerField(blank = True, null = True)
	# TYPE_CHOICES = (
		# ('new', 'new'),
		# ('old', 'old'),
	# )
	# type = models.CharField(max_length=30, choices=TYPE_CHOICES)
	# sum = models.DecimalField(max_digits=7, decimal_places=2)
	# datetime = models.DateTimeField(auto_now_add = True)
