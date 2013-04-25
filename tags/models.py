from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.core.urlresolvers import reverse


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_name': self.name})

    def __unicode__(self):
        return self.name


class ItemTag(models.Model):
    tag = models.ForeignKey('Tag')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    object = GenericForeignKey('content_type', 'object_it')

    class Meta:
        unique_together = ('tag', 'content_type', 'object_id')
