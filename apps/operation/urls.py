# _*_ coding:utf-8 _*_
from django.conf.urls import url, include
from .views import WriteArticleView,DeleteArticleView


urlpatterns = [

    url(r'^write/$',WriteArticleView.as_view(),name='operation_write'),
    # url(r'^editarticle/(?P<edit_article_id>\d+)/$',EditArticle.as_view(),name='edit_article')
    url(r'^delete/$',DeleteArticleView.as_view(),name='operation_delete'),
]