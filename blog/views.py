from django.shortcuts import render_to_response
from django.template import RequestContext

from blog.models import Article


def article(request, article_id):
	article = Article.objects.get(id=article_id)
	return render_to_response('blog/article.html', locals(),
		context_instance=RequestContext(request))
