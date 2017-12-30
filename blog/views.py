import random
import json
from io import BytesIO

from django.shortcuts import render,HttpResponse
from django.contrib import auth

from PIL import Image,ImageDraw,ImageFont


# Create your views here.


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
        if validCode.upper() == request.session.get("keepValidCode").upper():
            user = auth.authenticate(username=username, password=password)
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