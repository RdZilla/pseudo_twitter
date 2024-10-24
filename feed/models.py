from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Author(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Полное имя автора")
    registration_date = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.full_name


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст записи")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор записи")
    create_date = models.DateField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_text = models.CharField(max_length=200, verbose_name="Текст комментария")
    create_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор комментария")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=None, verbose_name="Запись")
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    count_of_likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        create_date = self.create_date.strftime("%d.%m.%Y")
        author_full_name = self.author.full_name
        return f"Комментарий от {create_date} от {author_full_name}"


class LikeOnComment(models.Model):
    LIKE = "&#128077;"
    CRY = "&#128557;"
    SURPRISE = "&#128562;"
    LAUGH = "&#128514;"
    HEARTH = "&#129505;"

    REACTIONS = (
        (LIKE, "like"),
        (CRY, "cry"),
        (SURPRISE, "surprise"),
        (LAUGH, "laugh"),
        (HEARTH, "hearth"),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=50, verbose_name="Текстовый код эмоции", choices=REACTIONS)
    create_date = models.DateField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Лайк на комментарии"
        verbose_name_plural = "Лайки на комментариях"
        unique_together = ['author', 'comment']

    def __str__(self):
        reaction = self.reaction
        author_fullname = self.author.full_name
        return f"{reaction} от {author_fullname}"
