from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "آخرین پست‌های بلاگ فرادرس کلون"
    link = "/blog/"
    description = "آخرین مقالات منتشر شده در بلاگ فرادرس کلون"

    def items(self):
        return Post.objects.filter(status='published').order_by('-published_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or item.content[:200]

    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.slug])