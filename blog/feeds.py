from django.contrib.syndication.views import Feed

from models import Article


class LatestArticles(Feed):
	title = "Ultimos artigos do blog."
	link = '/'
	title_template = 'feeds/latest_title.html'
	description_template = 'feeds/latest_description.html'

	def items(self):
		return Article.objects.all()

	def item_link(self, article):
		return '/rss/article/%d/' % article.id
