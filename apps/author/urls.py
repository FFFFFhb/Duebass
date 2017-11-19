# _*_ coding:utf-8 _*_
from django.conf.urls import url, include
from .views import AuthorListView


urlpatterns = [
    url(r'^author_list$',AuthorListView.as_view(), name='author_list'),
    url(r'^author_detail/(?P<article_id>\d+)/$',AuthorListView.as_view(), name='author_detail'),
]