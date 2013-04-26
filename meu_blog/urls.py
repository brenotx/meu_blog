from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.base import RedirectView

from blog.models import Article
from blog.feeds import LatestArticles

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ArchiveIndexView.as_view(model=Article, date_field="pub_date"), name="article_archive"),
    url(r'^rss/$', RedirectView.as_view(url='/rss/latest/')),
    url(r'^rss/latest/$', LatestArticles()),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'blog/', include('blog.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^tags/', include('tags.urls')),
    url(r'^bills/', include('bills.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, 'login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'}, 'logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'change_password.html'},
        name='change_password'),
    url(r'^change_password/success/$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'change_password_success.html'},
        name='change_password_success'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
