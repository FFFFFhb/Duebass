# _*_ coding:utf-8 _*_
from .models import Author
import xadmin

class AuthorAdmin(object):
    list_display = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(Author, AuthorAdmin)