from django.contrib import admin
from django import forms

from models import Article
from tags import apply_tags, tags_for_object


class ArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Article

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.initial['tags'] = tags_for_object(self.instance)


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

    def save_model(self, request, obj, form, change):
        super(ArticleAdmin, self).save_model(request, obj, form, change)

        apply_tags(obj, form.cleaned_data['tags'])


admin.site.register(Article, ArticleAdmin)
