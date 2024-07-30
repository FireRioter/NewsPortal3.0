from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import pgettext_lazy
from django.utils.translation import gettext as _


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comment_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']

        print(posts_rating)
        print('_______________')
        print(comments_rating)
        print('_______________')
        print(posts_comment_rating)

        self.rating = posts_rating * 3 + comments_rating + posts_comment_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_('category name'))

    def __str__(self):
        return self.name



class Post(models.Model):

    news = "NA"
    articles = "AR"

    POST_TYPES = [
        (news, "Новость"),
        (articles, "Статья")
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='posts',)
    poste_type = models.CharField(max_length=2, default=news)
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        text = self.text[:124]
        if len(self.text)> 124:
            text += '....'
        return text

    def __str__(self):
        return self.title


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class SubscriptionsCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)