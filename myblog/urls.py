"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings

from blog import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url (r'^cate/(?P<site_article_category>.*)/$',views.index),
    url(r'^login/$', views.sign_in),
    url(r'^logout/$', views.logout),
    url(r'^get_validCode/$', views.get_valid_code),
    url(r'^register/$', views.register),

    # 个人站点首页
    url(r'^blog/', include("blog.urls",namespace = "blog")),
    # 配置media
    url (r'^media/(?P<path>.*)$',serve,{"document_root":settings.MEDIA_ROOT}),

    #处理用户添加文章时上传的图片
    url(r'^uploadFile/$', views.uploadFile),
]
