# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

from billboard.models import Category

class Location(models.Model):
	title = models.CharField(unique=True, max_length=250)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['title']


AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False
AbstractUser._meta.get_field('first_name').blank = True
AbstractUser._meta.get_field('last_name').blank = True


class User(AbstractUser):
	phone = models.CharField(_('Phone'), max_length=256, help_text=_('Enter your phone number in this format +996 (555) 12-34-56'))
	url = models.CharField(_('Url'), max_length=512, blank=True)
	logo = models.ImageField(_('Photo or logo'), upload_to='accounts', null=True, blank=True)

	USER_TYPE_CHOICES = (
		(1, _('Build team')),
		(2, _('Seller')),
		(3, _('Master')),
		(4, _('Company')),
	)
	user_type = models.PositiveSmallIntegerField(_('Who are you?'), choices=USER_TYPE_CHOICES, max_length=1, default=2)
	user_category = models.ManyToManyField(Category, verbose_name=_('Type of works'), help_text=_(' '), blank=True, null=True)
	exp = models.PositiveSmallIntegerField(_('Experience'), null=True, blank=True, max_length=2)
	team_size = models.PositiveSmallIntegerField(_('Number of people in a team'), null=True, blank=True, max_length=3)
	year = models.PositiveIntegerField(_('On the market since'), null=True, blank=True, max_length=4)
	location = models.ForeignKey(Location, verbose_name=_('Location'), related_name='location', null=True, blank=True)
	delivery = models.BooleanField(_('Delivery'), default=False)

	objects = UserManager()

	def __unicode__(self):
		if self.first_name and self.last_name:
			return self.first_name + ' ' + self.last_name
		elif self.first_name:
			return self.first_name
		elif self.last_name:
			return self.last_name
		else:
			return self.username

	@models.permalink
	def get_absolute_url(self):
		return ('accounts_profile', (), {'username': self.username})
