from django.contrib.contenttypes.models import ContentType

from models import Tag, ItemTag


def apply_tags(obj, tags):
    dynamic_type = ContentType.objects.get_for_model(obj)

    ItemTag.objects.filter(
        content_type=dynamic_type,
        object_id=obj.id,
    ).delete()

    tags = tags.split(' ')
    for tag_name in tags:
        tag, new = Tag.objects.get_or_create(name=tag_name)

        ItemTag.objects.get_or_create(
            tag=tag,
            content_type=dynamic_type,
            object_id=obj.id,
        )

def tags_for_object(obj):
    dynamic_type = ContentType.objects.get_for_model(obj)

    tags = ItemTag.objects.filter(
        content_type=dynamic_type,
        object_id=obj.id,
    )

    return ' '.join([item.tag.name for item in tags])
