# _*_ encoding:utf-8 _*_
from datetime import datetime
from django.db import models

from users.models import UserProfile
from article.models import Article
# Create your models here.

class ArticleComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    article = models.ForeignKey(Article, verbose_name=u'文章')
    comments = models.CharField(max_length=200, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'评论时间')

    class Meta:
        verbose_name = u'文章评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    fav_id = models.IntegerField(default=0, verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1,'文章'),(2,'作者')), default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'收藏时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接收用户')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')
    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name