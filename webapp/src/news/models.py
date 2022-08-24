from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} | {self.rating}'

    def update_rating(self):
        ratings = Post.objects.filter(author_id=self.id)
        ratings = ratings.values('rating')
        ratings = list(ratings)
        result = 0

        for rat in ratings:
            result = rat['rating'] * 3 + result

        ratings = Comment.objects.filter(user_id=self.user_id)
        ratings = ratings.values('rating')
        ratings = list(ratings)

        for rat in ratings:
            result = rat['rating'] + result

        posts = Post.objects.filter(author_id=self.id)
        posts = posts.values('id')
        posts = list(posts)
        for post in posts:
            p = post['id']
            rats = Comment.objects.filter(id=p)
            rats = rats.values('rating')
            rats = list(rats)
            for rat in rats:
                result = rat['rating'] + result
                self.rating = result
                self.save()

        return result


class Category(models.Model):
    name = models.CharField(unique=True, max_length=128)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    article = 'AT'
    news = 'NS'

    TYPE = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    type = models.CharField(max_length=2, choices=TYPE, default=article)
    time_add = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        pass

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_add = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text} | {self.user}'




