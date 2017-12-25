from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserInfo(AbstractUser):
    '''
    用户表，继承AbstractUser,覆盖auth.user表
    '''
    nick_name = models.CharField(max_length=32,verbose_name="昵称")
    telephone = models.IntegerField(verbose_name="手机号")
    avatar = models.FileField(verbose_name="头像",upload_to="avatar",default="/avatar/default.png")
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username


class Blog(models.Model):
    '''
    个人站点
    '''
    title = models.CharField(max_length=64,verbose_name= "个人博客标题")
    site = models.CharField(max_length=32,verbose_name="个人博客后缀",unique=True)
    theme = models.CharField(max_length=32,verbose_name="博客主题")

    user = models.OneToOneField(to="UserInfo",verbose_name="所属用户")

    class Meta:
        verbose_name_plural = "博客表"
    def __str__(self):
        return self.title

class SiteCategory(models.Model):
    '''
    首页分类
    '''
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "网站分类"
    def __str__(self):
        return self.name

class SiteArticleCategory(models.Model):
    '''
    首页子分类
    '''
    name = models.CharField(max_length=32)
    site_category = models.ForeignKey(to="SiteCategory")

    class Meta:
        verbose_name_plural = "网站文章分类"

    def __str__(self):
        return self.name

class Category(models.Model):
    '''
    分类表
    '''
    title = models.CharField(max_length=32,verbose_name="文章类型")
    blog = models.ForeignKey(verbose_name="所属博客",to="Blog")

    class Meta:
        verbose_name_plural = "分类表"

    def __str__(self):
        return self.title

class Tag(models.Model):
    '''
    标签表
    '''
    title = models.CharField(max_length=32,verbose_name="标签名称")
    blog = models.ForeignKey(to="Blog",verbose_name="所属博客")

    class Meta:
        verbose_name_plural = "标签表"

    def __str__(self):
        return self.title

class Article(models.Model):
    '''
    文章表
    '''
    title = models.CharField(max_length=50,verbose_name="文章标题")
    desc = models.CharField(max_length=255,verbose_name="文章描述")
    read_count = models.IntegerField(verbose_name="评论数",default=0)
    comment_count = models.IntegerField(verbose_name="阅读数",default=0)
    up_count = models.IntegerField(verbose_name="点赞数",default=0)
    create_time = models.DateTimeField(verbose_name="创建时间")
    user = models.ForeignKey(to="UserInfo",verbose_name="所属用户")
    category = models.ForeignKey(to="Category",verbose_name="文章类型",null=True)
    #中介模型
    tag = models.ManyToManyField(
        to="Tag",
        verbose_name="文章标签",
        through="Article_Tag",
        through_fields=("article","tag")
    )
    site_article_category = models.ForeignKey(to="SiteArticleCategory",null=True,verbose_name="网站文章分类")

    class Meta:
        verbose_name_plural = "文章表"

    def __str__(self):
        return self.title

class Article_Tag(models.Model):
    '''
    文章标签关联表(中介模型)
    '''
    article = models.ForeignKey(to="Article",verbose_name="文章")
    tag = models.ForeignKey(to="Tag",verbose_name="标签")

    class Meta:
        #联合唯一
        unique_together = [
            ("article","tag"),

        ]
        verbose_name_plural = "文章标签关联表"
    def __str__(self):
        return self.article.title + "+" + self.tag.title


class ArticleDetail(models.Model):
    '''
    文章详情表
    '''
    content = models.TextField(verbose_name="文章内容")
    article = models.OneToOneField(to="Article",verbose_name="所属文章")

    class  Meta:
        verbose_name_plural = "文章详情表"
    def __str__(self):
        return self.content

class Comment(models.Model):
    '''
    用户评论表
    '''
    content = models.CharField(max_length=255,verbose_name="评论内容")
    content_time= models.DateTimeField(verbose_name="评论时间",auto_now_add=True)
    up_count = models.IntegerField(default=0,verbose_name="评论点赞")
    user = models.ForeignKey(to="UserInfo",verbose_name="评论者")
    article = models.ForeignKey(to="Article",verbose_name="评论文章")
    #自关联
    parent_comment = models.ForeignKey("self",verbose_name="父级评论",null=True,blank=True)

    class Meta:
        verbose_name_plural = "用户评论表"

    def __str__(self):
        return self.content

class CommentUp(models.Model):
    '''
    评论点赞表
    '''
    user = models.ForeignKey(to="UserInfo",verbose_name="点赞的用户")
    comment = models.ForeignKey(to='Comment',verbose_name="点赞的评论")

    class Meta:
        verbose_name_plural = "评论点赞表"

class ArticleUp(models.Model):
    '''
    文章点赞表
    '''
    user = models.ForeignKey(to='UserInfo',verbose_name="点赞的用户")
    article = models.ForeignKey(to="Article",verbose_name="点赞的文章")

    class Meta:
        verbose_name_plural = "文章点赞表"




