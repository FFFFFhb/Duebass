# _*_ coding:utf-8 _*_
import xadmin
from .models import ArticleComments,UserFavorite,UserMessage

class ArticleCommentsAdmin(object):
    list_display = ['user', 'article', 'comments', 'add_time']
    search_fields = ['user', 'article', 'comments']
    list_filter = ['user', 'article', 'comments', 'add_time']


xadmin.site.register(ArticleComments, ArticleCommentsAdmin)
class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']

xadmin.site.register(UserFavorite, UserFavoriteAdmin)
class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


xadmin.site.register(UserMessage, UserMessageAdmin)