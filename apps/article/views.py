from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
import json
from .models import Article
from operation.models import ArticleComments, UserFavorite
from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class ArticleListView(View):
    def get(self,request):
        all_articles = Article.objects.all()
        atc_nums = all_articles.count()
        hot_atcs = all_articles.order_by('-fav_nums')[:5]
        current_nav = 'article'
        #文章搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_articles = all_articles.filter(Q(title__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))


        sort = request.GET.get('sort','')
        if sort:
            if sort == 'fav_nums':
                all_articles = all_articles.order_by('-fav_nums')
            elif sort == 'add_time':
                all_articles = all_articles.order_by('-add_time')

    #对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_articles, 10, request=request)

        atcs = p.page(page)

        return render(request, 'article-list.html', {
            'all_articles': atcs,
            'atc_nums':atc_nums,
            'hot_atcs':hot_atcs,
            'sort': sort,
            'current_nav':current_nav,
        })

class ArticleDetailView(View):
    def get(self,request, article_id):
        article = Article.objects.get(id= int(article_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=article.id,fav_type=1):
                has_fav = True
        article.click_num += 1
        article.save()
        return render(request, 'article-detail.html', {
            'article':article,
            'has_fav':has_fav,
        })


class AddFavView(View):
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        if not request.user.is_authenticated():
            return  HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在，则取消收藏
            exist_records.delete()
            if int(fav_type)==1:
                article = Article.objects.get(id=int(fav_id))
                article.fav_nums -= 1
                if article.fav_nums < 0:
                    article.fav_nums = 0
                article.save()

            return  HttpResponse('{"status":"success", "msg":"收藏"}',content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0 :
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)

                user_fav.save()
                if int(fav_type) == 1:
                    article = Article.objects.get(id=int(fav_id))
                    article.fav_nums += 1
                    article.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class ArticleCommentView(View):
    def get(self,request, article_id):
        article = Article.objects.get(id= int(article_id))
        all_comments = ArticleComments.objects.all()
        article.click_num += 1
        article.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=article.id,fav_type=1):
                has_fav = True

        return render(request, 'article-comment.html', {
            'article':article,
            'all_comments': all_comments,
            'has_fav':has_fav,
        })

class AddCommentsView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            #判断用户登录状态
            # return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')
        article_id = request.POST.get('article_id',0)
        comments = request.POST.get('comments','')
        if int(article_id) > 0 and comments:
            article_comments = ArticleComments()
            article = Article.objects.get(id=int(article_id))
            article_comments.article = article
            article_comments.comments = comments
            article_comments.user = request.user
            article_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
        else:
            # return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')















