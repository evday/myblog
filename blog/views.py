import random
import json
import datetime
from io import BytesIO
import os

from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.db.models import Count,F
from django.db import transaction
from django.http import JsonResponse
from django.conf import settings

from PIL import Image,ImageDraw,ImageFont
from bs4 import BeautifulSoup

from blog.forms import RegisterForm
from blog import models
from myblog.utils.page import Pagination
from blog.forms import ArticleForm

# Create your views here.
def md5(val):
    '''
    md5 加密
    :param val:
    :return:
    '''
    import hashlib
    m = hashlib.md5()
    m.update(val.encode('utf-8'))
    return m.hexdigest()


def sign_in(request):
    '''
    登录
    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request,'login.html')
    elif request.method == "POST":
        state = {"state": None}
        username = request.POST.get("user")

        if username == "":
            state["state"] = "user_none"
            return HttpResponse(json.dumps(state))
        password = request.POST.get("pwd")

        if password == "":
            state["state"] = "pwd_none"
            return HttpResponse(json.dumps(state))

        validCode = request.POST.get("validCode")
        if validCode == "":
            state["state"] = "validCode_none"
            return HttpResponse(json.dumps(state))
        if validCode.upper() == request.session.get("ValidCode").upper():
            user = auth.authenticate(username=username,password=md5(password))
            if user:
                state["state"] = "success"
                auth.login(request, user)
            else:
                state["state"] = "failed"
            return HttpResponse(json.dumps(state))
        else:
            state["state"] = "validCode_error"
        return HttpResponse(json.dumps(state))

def logout(request):
    auth.logout(request)
    return redirect('/login/')

def get_valid_code(request):
    '''
    生成图片验证码
    :param request:
    :return:
    '''
    width = 400
    height = 40

    def color():
        '''
        生成随即颜色
        :return:
        '''
        return (random.randint(0,255),random.randint(10,255),random.randint(64,255))
    img = Image.new(mode = 'RGB',size = (120,40),color = "white")
    draw = ImageDraw.Draw(img,"RGB")
    font = ImageFont.truetype("static/font/kumo.ttf", 25)
    valid_code_list = []
    for i in range(5):#生成随机数字，字母
        random_num = str(random.randint(0,9))
        random_lower = chr(random.randint(65,90))
        random_upper = chr(random.randint(97,122))

        random_char = random.choice([random_num,random_lower,random_upper])

        draw.text([5+i*24,10],random_char,color(),font=font)
        valid_code_list.append(random_char)
    for i in range(100):#加噪点
        draw.point([random.randint(0,width),random.randint(0,height)],fill = color())
    for i in range(5):#加干扰线
        x1 = random.randint (0,width)
        y1 = random.randint (0,height)
        x2 = random.randint (0,width)
        y2 = random.randint (0,height)

        draw.line((x1,y1,x2,y2),fill = color())
    f = BytesIO()
    img.save(f,"png")
    data = f.getvalue()

    valid_str = ''.join(valid_code_list)
    print(valid_str)
    request.session["ValidCode"] = valid_str
    return HttpResponse(data)

def register(request):
    '''
    注册
    :param request:
    :return:
    '''
    if request.method == "GET":
        form = RegisterForm ()
        return render (request,'register.html',{"form":form})
    elif request.is_ajax ():

        form = RegisterForm (request.POST)
        registerResponse = {"user":None,"error_list":None}
        # print(type(form))
        if form.is_valid ():

            email = form.cleaned_data.get ("email")
            telephone = form.cleaned_data.get ("telephone")
            username = form.cleaned_data.get ("username")
            nick_name = form.cleaned_data.get ("nick_name")
            password = form.cleaned_data.get ("password")
            avatar_img = request.FILES.get ("avatar_img")

            models.UserInfo.objects.create_user (email = email,telephone = telephone,username = username,
                                                 nick_name = nick_name,password = md5(password),avatar = avatar_img)
            registerResponse ["user"] = form.cleaned_data.get ("username")

        else:
            registerResponse ["error_list"] = form.errors
        return HttpResponse (json.dumps (registerResponse))

def index(request,*args,**kwargs):
    '''
    网站首页
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    if kwargs:
        article_list = models.Article.objects.filter(site_article_category__name=kwargs.get("site_article_category"))
    else:
        article_list = models.Article.objects.all()
    cate_list = models.SiteCategory.objects.all()
    pager_obj = Pagination (request.GET.get ('page',1),len (article_list),request.path_info,request.GET)
    host_list = article_list [pager_obj.start:pager_obj.end]
    html = pager_obj.page_html ()
    return render(request,'index.html',{"article_list":host_list,"cate_list":cate_list,"page_html":html})


def homeSite(request,username,*args,**kwargs):
    '''
    个人站点
    :param request:
    :param username:
    :param args:
    :param kwargs:
    :return:
    '''

    current_user = models.UserInfo.objects.filter(username = username).first()

    current_blog = current_user.blog

    if not current_user:
        return render(request,'not_fond.html')

    # 查询当前用户的所有文章
    article_list = models.Article.objects.filter(user=current_user)

    # 查询当前用户的分档归类
    category_list = models.Category.objects.all().filter(blog=current_blog).annotate(c=Count("article__id")).values_list("title","c")

    # 查询当前用户的标签归类
    tag_list = models.Tag.objects.all().filter(blog=current_blog).annotate(c=Count("article__id")).values_list("title","c")

    # 查询当前用户的日期归类
    date_list = models.Article.objects.all().filter(user=current_user).extra(select = {
        "filter_create_time":"strftime('%%Y/%%m',create_time)"}).values_list("filter_create_time").annotate(Count("pk"))

    if kwargs:
        if kwargs.get("condition") == "category":
            article_list = models.Article.objects.filter(user=current_user,category__title=kwargs.get("para"))
        elif kwargs.get("condition") == "tag":
            article_list = models.Article.objects.filter(user=current_user,tag__title=kwargs.get("para"))
        elif kwargs.get("condition") == "date":
            year,month = kwargs.get("date").splite("/")
            article_list = models.Article.objects.filter(user=current_user,create_time__year=year,create_time__month=month)

    return render(request,'homeSite.html',locals())

def articleDetail(request,username,article_id):
    '''
    文章详情
    :param request:
    :param username:
    :param article_id:
    :return:
    '''
    models.Article.objects.filter(id=article_id).update(read_count = F("read_count")+1)
    current_user = models.UserInfo.objects.filter(username=username).first()
    print(current_user)
    current_blog = current_user.blog
    if not current_user:
        return render(request,'not_fond.html')

    # 查询当前用户的所有文章
    article_list = models.Article.objects.filter(user=current_user)

    #查询当前用户的分类归档
    category_list = models.Category.objects.all().filter(blog=current_blog).annotate(c = Count("article__id")).values_list("title","c")

    #查询当前用户的标签归档
    tag_list = models.Tag.objects.all().filter(blog= current_blog).annotate(c = Count("article__id")).values_list("title","c")

    #查询当前用户的日期归档
    date_list = models.Article.objects.all().filter(user=current_user).extra(select={
        "filter_create_time":"strftime('%%Y/%%m',create_time)"
    }).values_list("filter_create_time").annotate(Count("id"))

    article_obj = models.Article.objects.filter(id=article_id).first()
    obj = render (request,"articleDetail.html",locals ())
    obj.set_cookie ("user_username",request.user.username)#第一步将用户名放置到cookie中，这里是解决点赞之前登录
    obj.set_cookie ("next_path",request.path)
    return obj

def poll(request):
    '''
    点赞
    :param request:
    :return:
    '''
    pollResponse = {"status":True,"is_repeat":None,"user":None}
    if not request.user.is_authenticated():
        pollResponse["user"] = True
    else:
        user_id = request.user.id
        article_id = request.POST.get("article_id")
        if models.ArticleUp.objects.filter(user_id=user_id,article_id=article_id):
            pollResponse["is_repeat"] = True
            pollResponse["status"] = False
        else:
            try:
                with transaction.atomic():
                    models.ArticleUp.objects.create(user_id=user_id,article_id=article_id)
                    models.Article.objects.filter(id=article_id).update(up_count=F("up_count")+1)
            except:
                pollResponse["status"] = False
    return HttpResponse(json.dumps(pollResponse))

def article_comment(request):
    '''
    评论
    :param request:
    :return:
    '''
    response = {"user":None,"state":None,"create_time":None}
    if not request.user.is_authenticated():
        response["user"] = False
        return JsonResponse(response)
    user_id = request.POST.get("user_id")
    content = request.POST.get("comment_content")
    article_id = request.POST.get("article")

    #对评论进行评论
    if request.POST.get("parent_comment_id"):
        with transaction.atomic():
            pid = request.POST.get("parent_comment_id")
            comment_obj = models.Comment.objects.create(content=content,user_id=user_id,article_id=article_id,parent_comment_id=pid)
            response["create_time"] = str(comment_obj.content_time)
            response["parent_comment_username"] = comment_obj.parent_comment.user.username
            response["parent_comment_content"] = comment_obj.parent_comment.content
    else:
        with transaction.atomic():
            comment_obj = models.Comment.objects.create(content=content,user_id=user_id,article_id=article_id)
            models.Article.objects.filter(id=article_id).update(comment_count=F("comment_count")+1)

    response["comment_id"] = comment_obj.id
    response["create_time"] = str(comment_obj.content_time)
    return JsonResponse(response)

def backendIndex(request):
    '''
    个人后台
    :param request:
    :return:
    '''
    if not request.user.is_authenticated():
        return redirect('/login/')
    article_list = models.Article.objects.filter(user=request.user)
    return render(request,'backendIndex.html',{"article_list":article_list})



def addArticle(request):
    '''
    添加文章
    :param request:
    :return:
    '''
    if request.method == "GET":
        article_form = ArticleForm()
        cate_list = models.Category.objects.filter(blog__user = request.user)
        tag_list = models.Tag.objects.filter(blog__user = request.user)

        return render(request,"addArticle.html",locals())
    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            title = article_form.cleaned_data.get("title")
            content = article_form.cleaned_data.get("content")
            cate_obj = request.POST.get("cate_list")
            tag_obj_list = request.POST.getlist("tag_list")


            soup = BeautifulSoup (content,'html.parser')
            content_desc = soup.get_text () [:100]
            with transaction.atomic():
                article_obj = models.Article.objects.create(title=title,desc = content_desc,create_time=datetime.datetime.now(),user=request.user,category_id=cate_obj)
                models.ArticleDetail.objects.create(content=content,article=article_obj)

                if tag_obj_list:
                    for i in tag_obj_list:
                        models.Article_Tag.objects.create(article_id=article_obj.id,tag_id=i)

                return HttpResponse("添加成功")
    else:
        return render(request,'addArticle.html',locals())

def uploadFile(request):
        '''
        存储用户添加文章时上传的图片
        :param request:
        :return:
        '''
        file_obj = request.FILES.get("imgFile")
        file_name = file_obj.name

        #拼接文件存储路径
        path = os.path.join(settings.MEDIA_ROOT,"article_uploads",file_name)

        with open(path,"wb") as f:
            for i in file_obj.chunks():
                f.write(i)

        response = {
            "error":0,
            "url":"/media/article_uploads/"+file_name+"/"
        }
        return HttpResponse(json.dumps(response))