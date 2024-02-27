from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Expert(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Номер')
    name = models.CharField(null=False, max_length=64, verbose_name='ФИО')
    authority = models.FloatField(
        null=False,
        validators=[
            MaxValueValidator(1),
            MinValueValidator(0)
        ],
        verbose_name='Авторитет'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'



class Article(models.Model):
    IN_PROCESS = 0
    AGREED = 1
    EXPERTISE = -1

    ARTICLE_STATUS_CHOISES = {
        IN_PROCESS: "В процессе",
        AGREED: "Согласовано",
        EXPERTISE: "Дополнительная экспертиза",
    }
    
    uid = models.AutoField(primary_key=True, verbose_name='Номер')
    title = models.CharField(null=False, max_length=256, verbose_name='Название')
    author_full_name = models.CharField(null=False, max_length=64, verbose_name='Автор')
    status = models.IntegerField(choices=ARTICLE_STATUS_CHOISES, default=IN_PROCESS, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    def __str__(self) -> str:
        return f'"{self.title}"'
    
    def verbose(self):
        try:
            return Article.ARTICLE_STATUS_CHOISES[int(self.status)]
        except:
            return "-"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Marks(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Номер')
    expert_id = models.ForeignKey(Expert, on_delete=models.PROTECT, verbose_name='Эксперт')
    article_id = models.ForeignKey(Article, on_delete=models.PROTECT, verbose_name='Статья')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    total_mark = models.IntegerField(default=0, verbose_name='Итоговая оценка')
    pni_1 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПНИ_1',
        help_text='Соответствие предмета доклада тематике конференции',
    )
    pni_2 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПНИ_2',
        help_text='Научная новизна представляемого материала',
    )
    pni_3 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПНИ_3',
        help_text='Актуальность исследования',
    )
    pni_4 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПНИ_4',
        help_text='Обоснованность применяемых методов исследования',
    )
    pni_5 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПНИ_5',
        help_text='Обоснованность структуры статьи',
    )
    pni_6 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПНИ_6',
        help_text='Обоснованность и наглядность представленных рисунков, графиков и таблиц',
    )
    po_1 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПО_1',
        help_text='Соответствие оформленных материалов заданному шаблону',
    )
    po_2 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПО_2',
        help_text='Качество языка изложения',
    )
    po_3 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПО_3',
        help_text='Соответствие аннотации описанию работы',
    )
    po_4 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПО_4',
        help_text='Обоснованность и качество ключевых слов ',
    )
    po_5 = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='ПО_5',
        help_text='Список литературы: адекватность и правильность цитирования',
    )

    def __str__(self) -> str:
        return f"Итог: {self.total_mark}"
    
    def to_array(self)->list[int]:
        return [
            self.pni_1,
            self.pni_2,
            self.pni_3,
            self.pni_4,
            self.pni_5,
            self.pni_6,
            self.po_1,
            self.po_2,
            self.po_3,
            self.po_4,
            self.po_5,
        ]
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
