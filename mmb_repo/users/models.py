# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
# from django.utils.translation import ugettext_lazy as _

from mmb_repo.mmb_data.models import Genre, Instrument
from mmb_repo.mmb_data.utils import get_image_path

from .app_settings import CITIES, PHONE_REG

class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Profile(models.Model):
    user = models.ForeignKey(User)
    genre = models.ManyToManyField(Genre)
    instrument = models.ManyToManyField(Instrument)
    # todo - need list of all colleges if possible
    college = models.CharField(max_length=100, blank=True, null=True)
    current_city = models.CharField(choices=CITIES, max_length=50, blank=True, null=True)
    phone = models.CharField(validators=[PHONE_REG], max_length=10, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    about_me = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)

    def update(self,*args,**kwargs):
        self.college = kwargs.get('college')
        self.current_city = kwargs.get('current_city')
        self.phone = kwargs.get('phone')
        self.website = kwargs.get('website')
        self.about_me = kwargs.get('about_me')
        self.save()
