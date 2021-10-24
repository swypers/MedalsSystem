from django.db import models


sex_choice = [
    ('М', 'Мужской'),
    ('Ж', 'Женский')
]


class Status(models.Model):
    status = models.CharField(max_length=100, unique=True, verbose_name='Должность')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Rank(models.Model):
    name = models.CharField(max_length=50, verbose_name='Звание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Звание'
        verbose_name_plural = 'Звания'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория наград')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория наград'
        verbose_name_plural = 'Категории наград'

class Documents(models.Model):
    author = models.CharField(max_length=150, verbose_name='Автор приказа')
    num = models.IntegerField('Номер приказа')
    name = models.CharField(max_length=400, verbose_name='Название приказа', unique=True, blank=False)
    date = models.DateField(verbose_name='Дата издания', null=True, blank=True)
    description = models.CharField(max_length=300, verbose_name='Описание', null=True, blank=True)
    file = models.FileField(verbose_name='Файл', blank=True, upload_to='docs')

    def __str__(self):
        return 'Приказ МО №{} "{}"'.format(self.num, self.name)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['name']


class Medal(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название медали')
    image = models.FileField(upload_to='medals', verbose_name='Изображение')
    established = models.ForeignKey(Documents, on_delete=models.CASCADE, verbose_name='Учрежден')
    rules = models.TextField(verbose_name='Правила награждения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Медаль'
        verbose_name_plural = 'Медали'


class Soldier(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Должность')
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, verbose_name='Звание')
    F = models.CharField(max_length=50, verbose_name='Фамилия')
    I = models.CharField(max_length=50, verbose_name='Имя')
    O = models.CharField(max_length=50, verbose_name='Отчество')
    number = models.CharField(max_length= 20, verbose_name='Личный номер военнослужащего')
    sex = models.CharField(max_length=2, choices=sex_choice, default='М', verbose_name='Пол')
    date_of_birth = models.DateField('Дата рождения')
    place_of_birth = models.CharField(verbose_name='Место рождения', max_length=200)
    place_of_reg = models.CharField(verbose_name='Место регистрации', max_length=200)
    date_of_start = models.DateField('Дата начала прохождения службы')
    biography = models.TextField(verbose_name='Краткие биографические сведения',
                                 blank=True, default='')
    medals = models.ManyToManyField(Medal, blank=True, verbose_name='Награды')

    def __str__(self):  # Переопределили метод отображения офицера
        return '{0} {1}.{2}.'.format(self.F, self.I[0], self.O[0])

    class Meta:
        verbose_name = 'Военнослужащий'
        verbose_name_plural = 'Военнослужащие'
        ordering = ['F']
