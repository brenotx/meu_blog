from django.template import Library
from django.contrib.contenttypes.models import ContentType

from tags.models import ItemTag


register = Library()

@register.filter
def tags_for_object(object):
    dynamic_type = ContentType.objects.get_for_model(object)

    items = ItemTag.objects.filter(
        content_type=dynamic_type,
        object_id=object.id,
    )

    return [item.tag for item in items]
