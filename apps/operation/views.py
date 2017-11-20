from django.shortcuts import render
from django.views.generic.base import View
from utils.mixin_utils import LoginRequiredMixin
from .forms import NewArticleForm,NewArticleForm
import json
from django.http import HttpResponse,HttpResponseRedirect
from article.models import Article
from users.models import UserProfile
# Create your views here.
class WriteArticleView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request , 'new_article.html',{})
    def post(self,request):
        new_article_form = NewArticleForm(request.POST,request.FILES)
        if new_article_form.is_valid():
            image = new_article_form.cleaned_data['image']
            title = request.POST.get('title', '')
            desc = request.POST.get('desc', '')
            detail = request.POST.get('detail', '')
            author = request.user
            new_article = Article()
            new_article.author = author
            new_article.title = title
            new_article.image = image
            new_article.desc = desc
            new_article.detail = detail
            new_article.save()

            return render(request, 'success.html')
        else:
            return render(request, 'failde.html')

class DeleteArticleView(LoginRequiredMixin,View):
    def post(self,request):
        article_id = request.POST.get('article_id',0)

        if not request.user.is_authenticated():
            return  HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')
        exist_records = Article.objects.filter(pk=article_id)
        if exist_records:
            #如果记录已经存在，则取消收藏
            exist_records.delete()
            return render(request, 'success.html')

