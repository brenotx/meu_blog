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

# SIGNALS
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

@receiver(pre_save, sender=Article)
def article_pre_save(instance, sender, **kwargs):
    """ This signal create a slug automatic, verify if there is a article
    with the same slug name and add a number at end to avoid duplicity.
    """
    if not instance.slugs:
        slugs = slugify(instance.title)
        new_slugs = slugs
        cont = 0

        while Article.objects.filter(slugs=new_slugs).exclude(id=instance.id).count() > 0:
            cont += 1
            new_slugs = '%s-%d'%(slugs, cont)

        instance.slugs = new_slugs
