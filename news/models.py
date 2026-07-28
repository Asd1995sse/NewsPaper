from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг статей автора * 3
        posts_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        posts_rating *= 3

        # Суммарный рейтинг комментариев автора
        comments_rating = self.user.comment_set.aggregate(models.Sum('rating'))['rating__sum'] or 0

        # Суммарный рейтинг комментариев к статьям автора
        posts = self.post_set.values_list('id', flat=True)
        posts_comments_rating = Comment.objects.filter(post__in=posts).exclude(user=self.user).aggregate(
            models.Sum('rating'))['rating__sum'] or 0

        self.rating = posts_rating + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NE'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
    # Возвращает первые 124 символа текста, применимо в реальных моделях
    def preview(self):
        if len(self.content) > 124:
            return self.content[:124] + '...'
        return self.content


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()