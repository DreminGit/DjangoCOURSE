from blog.models import Post
from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_posts_from_cache():
    '''Получает данные о постах , и из кэша (если он вкл)'''
    if not CACHE_ENABLED:
        return Post.objects.all()
    key = 'post_list'
    posts = cache.get(key)
    if posts is not None:
        return posts
    posts = Post.objects.all()
    cache.set(key, posts)
    return posts