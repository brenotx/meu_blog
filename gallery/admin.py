try:
    import Image
except ImportError:
    from PIL import Image

from django.contrib import admin
from django import forms

from models import Album, Image
from tags import apply_tags, tags_for_object


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fiels = ('title',)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
    tags = forms.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.initial['tags'] = tags_for_object(
                self.instance)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('album', 'title',)
    list_filter = ('album',)
    search_fields = ('title', 'description',)
    form = ImageForm

    def save_model(self, request, obj, form, change):
        """
        This method create a thumbnail of an image and save it.

        """
        super(ImageAdmin, self).save_model(request, obj, form, change)
        if 'original' in form.changed_data:
            extension = obj.original.name.split('.')[-1]
            obj.thumbnail = 'gallery/thumbnail/%d.%s' % (obj.id, extension)
            miniature = Image.open(obj.original.path)
            miniature.thumbnail((100, 100), Image.ANTIALIAS)
            miniature.save(obj.thumbnail.path)
            obj.save()
        apply_tags(obj, form.cleaned_data['tags'])

admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)
