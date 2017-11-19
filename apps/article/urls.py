# _*_ coding:utf-8 _*_

from django.conf.urls import url, include
from .views import ArticleListView, ArticleDetailView, ArticleCommentView,AddCommentsView,AddFavView


urlpatterns = [
    url(r'^list$',ArticleListView.as_view(), name='article_list'),
    url(r'^detail/(?P<article_id>\d+)/$',ArticleDetailView.as_view(), name='article_detail'),
    #评论页
    url(r'^comment/(?P<article_id>\d+)/$',ArticleCommentView.as_view(), name='article_comment'),
    #添加课程评论
    url(r'^add_comment/$',AddCommentsView.as_view(), name='add_comment'),

    url(r'^add_fav/$',AddFavView.as_view(), name='add_fav')
]