from django.conf.urls import patterns, include, url


urlpatterns = patterns('gallery.views',
    url(r'^$', 'albums', name='gallery-albums'),
    url(r'^(?P<slugs>[\w_-]+)/$', 'album', name='gallery-album'),
    url(r'^image/(?P<slugs>[\w_-]+)/$', 'image', name='gallery-image')
)
