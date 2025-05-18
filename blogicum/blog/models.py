from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from .constants import CHAR_MAX_LENGTH, SLUG_MAX_LENGTH, STR_DISPLAY_MAX_LENGTH
from core.models import IsPublishedAbstract, CreatedAtAbstract
from .helpers import truncate_string


User = get_user_model()


class Category(IsPublishedAbstract, CreatedAtAbstract):
    title = models.CharField(
        "Заголовок",
        max_length=CHAR_MAX_LENGTH,
    )
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        max_length=SLUG_MAX_LENGTH,
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; разрешены символы "
            "латиницы, цифры, дефис и подчёркивание."
        )
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return truncate_string(self.title, STR_DISPLAY_MAX_LENGTH)


class Location(IsPublishedAbstract, CreatedAtAbstract):
    name = models.CharField(
        "Название места",
        max_length=CHAR_MAX_LENGTH,
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return truncate_string(self.name, STR_DISPLAY_MAX_LENGTH)


class Post(IsPublishedAbstract, CreatedAtAbstract):
    title = models.CharField(
        "Заголовок",
        max_length=CHAR_MAX_LENGTH,
    )
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        default=timezone.now,
        help_text=(
            "Если установить дату и время в будущем "
            "— можно делать отложенные публикации."
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts",
    )
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Местоположение",
        related_name="posts",
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        related_name="posts",
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ('-pub_date',)

    def __str__(self):
        return truncate_string(self.title, STR_DISPLAY_MAX_LENGTH)


class Comment(CreatedAtAbstract):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name="Публикация"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comments",
    )
    text = models.TextField("Текст комментария")

    class Meta(CreatedAtAbstract.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return truncate_string(self.post.title, STR_DISPLAY_MAX_LENGTH)
