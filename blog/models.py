from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now(), blank=True)
    slugs = models.SlugField(max_length=100, blank=True, unique=True)

    class Meta:
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse('blog.views.article', kwargs={'slugs': self.slugs})

    def __unicode(self):
        return self.title

# SIGNALS
from django.db.models.signals import pre_save
from utils.commonSignals import slug_pre_save

pre_save.connect(slug_pre_save, sender=Article)
