# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
import json
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm,UploadImageForm,YonghuInfoForm
from operation.forms import EditArticleForm
from utils.email_send import send_register_email
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from article.models import Article
from django.http import HttpResponse,HttpResponseRedirect
from operation.models import UserFavorite
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')

        return render(request, 'login.html')


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form,'msg': '用户已存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户名未激活!'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误或未激活!'})
        else:
            return render(request, 'login.html', {'login_form':login_form})

class LogoutView(View):
    #用户登出
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))

class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email,send_type='forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form':forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    #修改用户密码
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email':email, 'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})

class YonghuListView(View):
    def get(self,request):
        all_yonghu = UserProfile.objects.all()
        yonghu_nums = all_yonghu.count()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_yonghu = all_yonghu.filter(
                Q(username__icontains=search_keywords) | Q(gender__icontains=search_keywords) | Q(
                    age__icontains=search_keywords))

        sort = request.GET.get('sort','')
        if sort:
            all_yonghu = all_yonghu.order_by('-fans_nums')

#对用户进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_yonghu, 10, request=request)
        yonghu = p.page(page)

        return render(request, 'users-list.html', {
            'all_yonghu':yonghu,
            'sort':sort,
            'yonghu_nums':yonghu_nums,
        })

class YonghuDetailView(View):
    def get(self,request,yonghu_id):
        yonghu = UserProfile.objects.get(id=int(yonghu_id))
        all_article = Article.objects.filter(author=yonghu)
        has_fav_yonghu = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=yonghu.id, fav_type=2):
                has_fav_yonghu = True
        return render(request, 'user-detail.html', {
            'yonghu':yonghu,
            'all_article':all_article,
            'has_fav_yonghu': has_fav_yonghu,
        })

class AddFavYonghuView(View):
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)


        if not request.user.is_authenticated():
            return  HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在，则取消收藏
            exist_records.delete()
            if int(fav_type)==2:
                user = UserProfile.objects.get(id=int(fav_id))
                user.fans_nums -= 1
                if user.fans_nums < 0:
                    user.fans_nums = 0
                user.save()
            return  HttpResponse('{"status":"success", "msg":"关注"}',content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0 :
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 2:
                    user = UserProfile.objects.get(id=int(fav_id))
                    user.fans_nums += 1
                    user.save()
                return HttpResponse('{"status":"success", "msg":"已关注"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail", "msg":"关注出错"}', content_type='application/json')

class YonghuInfoView(LoginRequiredMixin,View):
    #用户个人信息
    def get(self,request):
        return render(request,'usercenter-info.html',{})
    def post(self,request):
        user_info_form = YonghuInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageView(LoginRequiredMixin,View):
    #用户修改头像
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class UpdatePwdView(View):
    #在个人中心修改用户密码
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')

            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin,View):
    #发送邮箱验证码
    def get(self,request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')

class UpdateEmailView(LoginRequiredMixin,View):
    #修改个人邮箱
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')

class MyArticleView(LoginRequiredMixin,View):
    #我的文章
    def get(self,request):
        user_articles = Article.objects.filter(author=request.user)
        return render(request, 'usercenter-myarticle.html', {
            'user_articles':user_articles
        })

class MyFavAtcView(LoginRequiredMixin,View):
    #我收藏的文章
    def get(self,request):
        atc_list = []
        fav_atcs = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_atc in fav_atcs:
            atc_id = fav_atc.fav_id
            atc = Article.objects.get(id=atc_id)
            atc_list.append(atc)
        return render(request, 'usercenter-fav-article.html', {
            'atc_list':atc_list
        })

class MyFavUserView(LoginRequiredMixin,View):
    #我关注的用户
    def get(self,request):
        user_list = []
        fav_users = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_user in fav_users:
            user_id = fav_user.fav_id
            user = UserProfile.objects.get(id=user_id)
            user_list.append(user)
        return render(request, 'usercenter-fav-user.html', {
            'user_list':user_list
        })

class EditArticle(LoginRequiredMixin,View):
    def get(self,request,edit_article_id):
        article = Article.objects.get(id=int(edit_article_id))
        return render(request,'edit_article.html',{
            'article':article,
        })
    def post(self,request,edit_article_id):
        edit_article = EditArticleForm(request.POST,request.FILES)
        if edit_article.is_valid():
            image = edit_article.cleaned_data['image']
            title = request.POST.get('title', '')
            desc = request.POST.get('desc', '')
            detail = request.POST.get('detail', '')
            edit_article = Article.objects.get(pk=edit_article_id)
            edit_article.title = title
            if image:
                edit_article.image = image
            edit_article.desc = desc
            edit_article.detail = detail
            edit_article.save()

            return render(request, 'success.html')
        else:
            return render(request, 'failde.html')


class SuccessView(View):
    def get(self,request):
        return render(request,'success.html')
class FailedView(View):
    def get(self,request):
        return render(request,'failde.html')