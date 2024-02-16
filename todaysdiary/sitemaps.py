from django.urls import reverse
from django.contrib.sitemaps import Sitemap 
from posts.models import Post
from django.db.models import Q


class StaticViewSitemap(Sitemap): 
    priority = 0.5 
    changefreq = 'weekly' 
    
    def items(self): 
        return [ 
            'base:index',
            'base:everydiary',
            'base:intro',
            'base:notice',
            'base:qna',
            'base:contact',
            'topics:topic',
            'users:signup',
            'users:login',
        ]
        
    def location(self, item): 
        return reverse(item)


class SnippetViewSitemap(Sitemap): 
    priority = 0.5 
    changefreq = 'weekly' 
    
    def items(self): 
        return Post.objects.filter(Q(public="public"))
