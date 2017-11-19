# _*_ encoding:utf-8 _*_
from datetime import datetime
from django.db import models

from users.models import UserProfile

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name=u'作者', null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name=u'文章名')
    desc = models.CharField(max_length=100, verbose_name=u'文章描述')
    detail = models.TextField(verbose_name=u'文章详情')
    reader = models.IntegerField(default=0, verbose_name=u'阅读人数')
    fav_nums =models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='article/%Y/%m', verbose_name=u'封面图', max_length=100,null=True, blank=True)
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title