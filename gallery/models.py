from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime


class Album(models.Model):
    title = models.CharField(max_length=100)
    slugs = models.SlugField(max_length=100, blank=True, unique=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery.views.album', kwargs={'slugs': self.slugs})


class Image(models.Model):
    """
    Each instance of this class contain an image of gallery, with its
    repective thumbnail and natural image size. Several imagens may contain
    inside of an Album.

    """

    album = models.ForeignKey('Album',)
    title = models.CharField(max_length=100)
    slugs = models.SlugField(max_length=100, blank=True, unique=True)
    description = models.TextField(blank=True)
    original = models.ImageField(
        null=True,
        blank=True,
        upload_to='gallery/original',
    )
    thumbnail = models.ImageField(
        null=True,
        blank=True,
        upload_to='gallery/thumbnail',
    )
    pub_date = models.DateTimeField(default=datetime.now(), blank=True)

    class Meta:
        ordering = ('album', 'title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery.views.image', kwargs={'slugs': self.slugs})

# SIGNALS
from django.db.models.signals import pre_save
from utils.commonSignals import slug_pre_save


pre_save.connect(slug_pre_save, sender=Album)
pre_save.connect(slug_pre_save, sender=Image)
