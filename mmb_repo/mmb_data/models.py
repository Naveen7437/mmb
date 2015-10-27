from django.db import models
from config.settings.common import AUTH_USER_MODEL

# from mmb_repo.users.models import User
from .app_settings import SONG_TAGS

class Genre(models.Model):
    genre = models.CharField(max_length=30)

    def __unicode__(self):
        return '{}'.format(self.genre)


class Instrument(models.Model):
    instrument = models.CharField(max_length=30)
    # level = models.CharField(choices=SKILL_LEVEL, default='Beginner')

    def __unicode__(self):
        return '{}'.format(self.instrument)
#
def get_upload_path(instance,f):
    return "audio/{}/{}/".format(instance.id,f)


# class Band(models.Model):
#     name = models.CharField(blank=True, max_length=255)
#     desc = models.CharField(blank=True, max_length=255)
#     users = models.ManyToManyField(User)
#     band_genre = models.ForeignKey(Genre)
#     #tags - can't remember
#
#
# class Followers(models.Model):
#     follower = models.ForeignKey(User)
#     follower_is_user = models.BooleanField()
#     following = models.ForeignKey(User)
#     following_is_user = models.BooleanField()

class Songs(models.Model):
    # type = models.CharField(choices=SONG_TYPES, default='Audio')
    user = models.ForeignKey(AUTH_USER_MODEL)
    tags = models.CharField(choices=SONG_TAGS, max_length=255)
    name = models.CharField(max_length=255)
    upload = models.FileField(upload_to="audio/")
    # singer = models.CharField(blank=True, max_length=255)
    # label = models.CharField(blank=True, max_length=255)
    def __unicode__(self):
        return '{}'.format(self.name)
