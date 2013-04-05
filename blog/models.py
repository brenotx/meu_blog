from django.db import models
from datetime import datetime


class Article(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	pub_date = models.DateTimeField(default=datetime.now(), blank=True)

	class Meta:
		ordering = ('-pub_date',)
