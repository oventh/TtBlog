from django.db import models

# Create your models here.

class User(models.Model):
    Id = models.IntegerField(primary_key=True)
    Username = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=50, unique=True)
    Nickname = models.CharField(max_length=50, unique=True)
    Email = models.EmailField()
    Type = models.IntegerField(unique=True)
    CreateTime = models.DateTimeField(unique=True)
    Enable = models.BooleanField(unique=True)


class Site(models.Model):
    Id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100, unique=True)
    Summary = models.CharField(max_length=300)
    Banner = models.CharField(max_length=500, unique=False)
    PageSize = models.IntegerField()


class Post(models.Model):
    Id = models.IntegerField(primary_key=True)
    User = models.ForeignKey("User", on_delete=models.CASCADE,)
    Title = models.CharField(max_length=100, unique=True)
    Banner = models.CharField(max_length=500, unique=False)
    Summary = models.CharField(max_length=300)
    Content = models.TextField(unique=True)
    CreateTime = models.DateTimeField(unique=True)
    CanComment = models.BooleanField(unique=True)
    Categories = models.ManyToManyField("Category")
    Tags = models.ManyToManyField("Tag")


class Category(models.Model):
    Id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=50, unique=True)


class Comment(models.Model):
    Id = models.IntegerField(primary_key=True)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    ReComment = models.ForeignKey('Comment', on_delete=models.CASCADE,)
    Content = models.TextField(unique=True)
    CreateTime = models.DateTimeField(unique=True)
    Creator = models.CharField(max_length=50, unique=True)


class Tag(models.Model):
    Id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=20, unique=True)


