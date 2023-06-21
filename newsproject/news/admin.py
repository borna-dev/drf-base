from django.contrib import admin
from news.models import Article, Journalist, Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(Journalist)
admin.site.register(Comment)
