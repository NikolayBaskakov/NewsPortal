from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

# Create your models here.
        
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    
    def update_rating(self):
        article_raiting = 0
        for i in Post.objects.filter(type = 'AR', author = self):
            article_raiting += i.rating
        article_raiting *= 3
        from_comment_rating = 0
        for i in Comment.objects.filter(user= self.user):
            from_comment_rating += i.rating
        to_comment_rating = 0
        for i in Comment.objects.all():
            if i.post.author == self:
                to_comment_rating += i.rating
        self.rating = article_raiting + from_comment_rating + to_comment_rating
        self.save()
        
    def __str__(self) -> str:
        return f'{self.user.username}'
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
class Post(models.Model):
    article = 'AR'
    news = "NW"

    TYPES = [(article, 'Статья'),
             (news, 'Новость')]
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type = models.CharField(max_length= 2, choices=TYPES, default=news)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
        
    def preview(self):
        return str(self.text)[:124] + '...'
        self.save()
        
    def __str__(self) -> str:
        return f'{self.title[:20]}'

class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating +=1
        self.save()
    
    def dislike(self):
        self.rating -=1
        self.save()
        
    def __str__(self) -> str:
        return f'{self.text[:15]}'
        
        
class Subscriber(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriber')
    category= models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriber')