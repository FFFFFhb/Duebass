# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models

# Create your models here.
class Author(models.Model):

    name = models.CharField(max_length=50, verbose_name=u'作者名')
    work_years = models.IntegerField(default=0, verbose_name=u'使用年限')
    work_company = models.CharField(max_length=50, verbose_name=u'公司/学校')
    work_position = models.CharField(max_length=50, verbose_name=u'职位')
    points = models.CharField(max_length=50, verbose_name=u'个人特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name