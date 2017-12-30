from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserInfo)
admin.site.register(models.Blog)
admin.site.register(models.Article)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.CommentUp)
admin.site.register(models.Category)
admin.site.register(models.SiteCategory)
admin.site.register(models.SiteArticleCategory)
admin.site.register(models.ArticleUp)
admin.site.register(models.Article_Tag)