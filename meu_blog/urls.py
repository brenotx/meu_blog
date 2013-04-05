from django.conf.urls import patterns, include, url
from django.views.generic.dates import ArchiveIndexView

from blog.models import Article
from blog.feeds import LatestArticles

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 
		ArchiveIndexView.as_view(model=Article, date_field="pub_date"),
		name="article_archive"),
	url('^rss/latest/$', LatestArticles()),
	url('^rss/article/(?P<article_id>\d+)/$', 'blog.views.article'),
    url(r'^admin/', include(admin.site.urls)),
)
