from django.db import models
from django.contrib.auth.models import User


class Journalist(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'


class Article(models.Model):
    # author = models.CharField(max_length=100)
    # check data migration
    author = models.ForeignKey(Journalist, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    main_text = models.TextField()
    published_time = models.DateField()
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title} - {self.author}'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.article} - {self.comment[:20]}'
