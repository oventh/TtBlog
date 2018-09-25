from django.db import models

# Create your models here.

class User(models.Model):
    Id = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=50, null = False)
    Nickname = models.CharField(max_length=50, null = False)
    Email = models.EmailField()
    Type = models.IntegerField(null = False)
    CreateTime = models.DateTimeField(null = False)
    Enable = models.BooleanField(null = False)


class Site(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, null = False)
    Summary = models.CharField(max_length=300, null = True)
    Banner = models.CharField(max_length=500, null = True)
    PageSize = models.IntegerField(null = True)


class Post(models.Model):
    Id = models.AutoField(primary_key=True)
    User = models.ForeignKey("User", on_delete=models.CASCADE,)
    Title = models.CharField(max_length=100, null = False)
    Banner = models.CharField(max_length=500, null = False)
    Summary = models.CharField(max_length=300, null = True)
    Content = models.TextField(null = False)
    CreateTime = models.DateTimeField(null = False)
    CanComment = models.BooleanField(null = False)
    Categories = models.ManyToManyField("Category")
    Tags = models.ManyToManyField("Tag")


class Category(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null = False)


class Comment(models.Model):
    Id = models.AutoField(primary_key=True)    
    Post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    ReComment = models.ForeignKey('Comment', on_delete=models.CASCADE,)
    Content = models.TextField(null = False)
    CreateTime = models.DateTimeField(null = False)
    Creator = models.CharField(max_length=50, null = False)


class Tag(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20, null = False)


