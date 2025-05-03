from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class PostCategory(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_choices = [
        ('article', 'Статья'),
        ('news', 'Новость')
    ]
    type = models.CharField(max_length=7, choices=type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title[:124]}..."

    # Методы для изменения рейтинга
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # Метод предварительного просмотра текста поста
    def preview(self):
        text_post = str(self.content.value_from_object(self))
        if len(text_post) > 124:
            return f'{self.content[:124]}...'
        else:
            return self.content


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'Комментарий от {self.user.username}'

    # Методы для изменения рейтинга
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()