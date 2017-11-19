# _*_ coding:utf-8 _*_
from .models import Article
import xadmin

class ArticleAdmin(object):
    list_display = ['title', 'desc', 'detail', 'reader', 'fav_nums', 'image', 'click_num', 'add_time']
    search_fields = ['title', 'desc', 'detail', 'reader', 'fav_nums', 'image', 'click_num']
    list_filter = ['title', 'desc', 'detail', 'reader', 'fav_nums', 'image', 'click_num', 'add_time']

xadmin.site.register(Article, ArticleAdmin)