from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """Обновляем рейтинг автора"""
        # 1. Сумма рейтингов статей автора, умноженная на 3
        posts_rating = sum(post.rating for post in Post.objects.filter(author=self)) * 3

        # 2. Рейтинг комментариев самого автора
        own_comments_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))

        # 3. Рейтинг комментариев к статьям автора
        comments_to_posts_rating = sum(comment.rating for comment in Comment.objects.filter(post__author=self))

        # Итоговый рейтинг
        self.rating = posts_rating + own_comments_rating + comments_to_posts_rating
        self.save()


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
        text_content = self.content  # Получаем содержимое поля
        if len(str(text_content)) > 124:
            return f'{text_content[:124]}...'
        else:
            return text_content


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
