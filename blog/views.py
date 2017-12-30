import random
import json
from io import BytesIO

from django.shortcuts import render,HttpResponse
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password

from PIL import Image,ImageDraw,ImageFont

from blog.forms import RegisterForm
from blog import models

# Create your views here.
def md5(val):
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
    if kwargs:
        article_list = models.Article.objects.filter(site_article_category__name=kwargs.get("site_article_category"))
    else:
        article_list = models.Article.objects.all()
    cate_list = models.SiteCategory.objects.all()
    return render(request,'index.html',{"article_list":article_list,"cate_list":cate_list})


def homeSite(request):
    pass