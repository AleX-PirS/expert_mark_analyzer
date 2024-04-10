from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

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
    h_index = models.IntegerField(default=-1, verbose_name='Индекс Хирша')
    role = models.IntegerField(choices=USER_ROLE_CHOISES, default=NONE, verbose_name='Роль')
    about = models.TextField(default='', verbose_name='Персональная информация')
    birthday = models.DateField(default=datetime.date(1, 1, 1), verbose_name='Дата рождения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        return f"{self.get_full_name()}"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Theme(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    title = models.CharField(unique=True, null=False, max_length=128, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Тематика'
        verbose_name_plural = 'Тематики'

class UserTheme(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='user_id')
    theme_id = models.ForeignKey(Theme, on_delete=models.DO_NOTHING, verbose_name='theme_id')
    class Meta:
        verbose_name = 'Пользователь_тематика'
        verbose_name_plural = 'Пользователь_тематика'

class Criteria(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    title = models.CharField(unique=True, null=False, max_length=128, verbose_name='Название')
    max_value = models.FloatField(null=False, verbose_name='Максимальное значение')
    min_value = models.FloatField(null=False, verbose_name='Минимальное значение')
    about = models.CharField(default="", max_length=256, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Критерий'
        verbose_name_plural = 'Критерии'

class MarkList(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    title = models.CharField(unique=True, null=False, max_length=128, verbose_name='Название')
    coherence_factor = models.FloatField(default=0.7, validators=[MaxValueValidator(1.0),MinValueValidator(0.001)], verbose_name='Фактор согласованности')
    necessary_experts_number = models.IntegerField(default=3, validators=[MaxValueValidator(999),MinValueValidator(1)], verbose_name='Количество экспертов')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Набор оценок'
        verbose_name_plural = 'Наборы оценок'

class MarkListCriteria(models.Model):
    weight = models.FloatField(default=1.0, validators=[MaxValueValidator(1.0),MinValueValidator(0.001)], verbose_name='Вес')
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
    created_by = models.ForeignKey(User, default="", on_delete=models.DO_NOTHING, verbose_name="Добавил")
    author = models.CharField(null=False, max_length=256, verbose_name='Автор')
    title = models.CharField(null=False, max_length=256, verbose_name='Название')
    link = models.CharField(null=False, max_length=512, verbose_name='Статья')
    theme_id = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='Тематика')
    status = models.IntegerField(choices=STATUS_CHOISES, default=UNALLOCATED, verbose_name='Статус')
    total_mark = models.FloatField(default=0, verbose_name='Итог')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Score(models.Model):
    ON_MARK = 0
    REJECTED = 1
    DONE = 2

    STATUS_CHOISES = {
        ON_MARK: "На оценке",
        REJECTED: "Нет согласования оценки",
        DONE: "Оценена",
    }
    uid = models.AutoField(primary_key=True, verbose_name='Id')
    expert_id = models.ForeignKey(User, default="", on_delete=models.DO_NOTHING, verbose_name='Эксперт')
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    mark_list_id = models.ForeignKey(MarkList, on_delete=models.CASCADE, verbose_name='Критерии')
    status = models.IntegerField(choices=STATUS_CHOISES, default=ON_MARK, verbose_name='Статус')
    review = models.TextField(null=False, verbose_name='Ревью')
    total_mark = models.FloatField(default=0, verbose_name='Итог')
    reject_reason = models.CharField(default='', max_length=1024, verbose_name='Причина отмены')
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
