from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(auth_models.User):
    NONE = 0
    EXPERT = 1
    WORKER = 2

    USER_ROLE_CHOISES = {
        NONE: "Пустая роль",
        EXPERT: "Эксперт",
        WORKER: "Обработчик статей",
    }
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    h_index = models.IntegerField(null=False, verbose_name='Индекс Хирша')
    role = models.IntegerField(choices=USER_ROLE_CHOISES, default=NONE, verbose_name='Роль')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        return f"{self.get_full_name()}"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Theme(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    title = models.CharField(null=False, max_length=128, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Тематика'
        verbose_name_plural = 'Тематики'

class UserTheme(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user_id')
    theme_id = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='theme_id')
    class Meta:
        verbose_name = 'Пользователь_тематика'
        verbose_name_plural = 'Пользователь_тематика'

class Criteria(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    title = models.CharField(null=False, max_length=128, verbose_name='Название')
    max_value = models.FloatField(null=False, verbose_name='Максимальное значение')
    min_value = models.FloatField(null=False, verbose_name='Минимальное значение')
    weight = models.FloatField(default=1.0, validators=[MaxValueValidator(1.0),MinValueValidator(0.001)], verbose_name='Вес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Критерий'
        verbose_name_plural = 'Критерии'

class MarkList(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    title = models.CharField(null=False, max_length=128, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Набор оценок'
        verbose_name_plural = 'Наборы оценок'

class MarkListCriteria(models.Model):
    mark_list_id = models.ForeignKey(MarkList, on_delete=models.CASCADE, verbose_name='mark_list_id')
    criteria_id = models.ForeignKey(Criteria, on_delete=models.CASCADE, verbose_name='criteria_id')
    class Meta:
        verbose_name = 'Набор_оценок_критерий'
        verbose_name_plural = 'Набор_оценок_критерий'

class Article(models.Model):
    UNALLOCATED = 0
    ON_MARK = 1
    MARKED = 2

    STATUS_CHOISES = {
        UNALLOCATED: "Не распределена",
        ON_MARK: "На оценке",
        MARKED: "Оценена",
    }
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    title = models.CharField(null=False, max_length=256, verbose_name='Название')
    link = models.CharField(null=False, max_length=512, verbose_name='Статья')
    status = models.IntegerField(choices=STATUS_CHOISES, default=UNALLOCATED, verbose_name='Статус')
    total_mark = models.FloatField(default=0, verbose_name='Итог')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class ArticleTheme(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='article_id')
    theme_id = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='theme_id')
    class Meta:
        verbose_name = 'Статья_тематика'
        verbose_name_plural = 'Статья_тематика'

class Score(models.Model):
    ON_MARK = 0
    REJECTED = 1

    STATUS_CHOISES = {
        ON_MARK: "На оценке",
        REJECTED: "Нет согласования оценки",
    }
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    expert_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Эксперт')
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    mark_list_id = models.ForeignKey(MarkList, on_delete=models.CASCADE, verbose_name='Критерии')
    status = models.IntegerField(choices=STATUS_CHOISES, default=ON_MARK, verbose_name='Статус')
    total_mark = models.FloatField(default=0, verbose_name='Итог')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')
    
    def __str__(self) -> str:
        return f"{self.total_mark}"
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

class ScoreCriteria(models.Model):
    score_id = models.ForeignKey(Score, on_delete=models.CASCADE, verbose_name='score_id')
    criteria_id = models.ForeignKey(Criteria, on_delete=models.CASCADE, verbose_name='criteria_id')
    value = models.FloatField(null=False, verbose_name='Значение')
    class Meta:
        verbose_name = 'Оценка_критерий'
        verbose_name_plural = 'Оценка_критерий'
