from django.template.defaultfilters import slugify

def slug_pre_save(instance, sender, **kwargs):
    """ This signal create a slug automatic, verify if there is a article
    with the same slug name and add a number at end to avoid duplicity.
    """
    if not instance.slugs:
        slugs = slugify(instance.title)
        new_slugs = slugs
        cont = 0

        while sender.objects.filter(slugs=new_slugs).exclude(id=instance.id).count() > 0:
            cont += 1
            new_slugs = '%s-%d'%(slugs, cont)

        instance.slugs = new_slugs
