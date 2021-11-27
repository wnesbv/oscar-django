from django.contrib.sitemaps import Sitemap
from articles.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.filter(title=False)

    def lastmod(self, obj):
        return obj.timestamp
