# _*_ coding:utf-8 _*_
from django.conf.urls import url, include
from .views import YonghuListView,YonghuDetailView,AddFavYonghuView,YonghuInfoView,UploadImageView,UpdatePwdView
from .views import SendEmailCodeView,UpdateEmailView,MyArticleView,MyFavAtcView,MyFavUserView,EditArticle

urlpatterns = [
    url(r'^list$',YonghuListView.as_view(), name='yonghu_list'),
    url(r'^detail/(?P<yonghu_id>\d+)/$',YonghuDetailView.as_view(), name='yonghu_detail'),
    url(r'^add_fav_yonghu/$',AddFavYonghuView.as_view(), name='add_fav_yonghu'),
    #用户信息
    url(r'^info/$',YonghuInfoView.as_view(),name='yonghu_info'),
   #用户头像上传
    url(r'image/upload/$',UploadImageView.as_view(),name='image_upload'),
    #用户修改密码
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name="update_pwd"),
    #发送邮箱验证码
    url(r'^sendemail_code/$',SendEmailCodeView.as_view(),name='sendemail_code'),
    #修改邮箱
    url(r'^update_email/$',UpdateEmailView.as_view(),name='update_email'),

    # 我的文章
    url(r'^myarticle/$', MyArticleView.as_view(), name='myarticle'),
    # 我的收藏的文章
    url(r'^myfav/atc$', MyFavAtcView.as_view(), name='myfav_atc'),
    # 我的关注的文章
    url(r'^myfav/user$', MyFavUserView.as_view(), name='myfav_user'),
    #修改文章
    url(r'^editarticle/(?P<edit_article_id>\d+)/$', EditArticle.as_view(), name='editarticle'),

]