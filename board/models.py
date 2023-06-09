from django.db import models
from django.contrib.auth.models import User

POSITION_TYPE = (
    ('Tank', 'Танки'),
    ('Healer', 'Хилы'),
    ('DD', 'ДД'),
    ('Merchant', 'Торговцы'),
    ('Guildmaster', 'Гилдмастеры'),
    ('QuestGiver', 'Квестгиверы'),
    ('Blacksmith', 'Кузнецы'),
    ('Skinner', 'Кожевники'),
    ('PotionMaster', 'Зельевары'),
    ('SpellMaster', 'Мастер заклинаний'),
)


#        Модель Category. Категории объявлений. Имеет единственное поле: название категории.
class Category(models.Model):
    category_name = models.CharField(max_length=32, choices=POSITION_TYPE, unique=True)

    def __str__(self):
        return f'{self.category_name}'


#        Модель Bulletin. Объявления пользователей.
#        Каждый объект может иметь одну категорию.
#        Соответственно, модель должна включать следующие поля:
#                связь «один ко многим» с моделью User;
#                автоматически добавляемая дата и время создания;
#                связь «один ко многим» с моделью Category;
#                заголовок объявления;
#                текст объявления;
#        Метод preview() возвращает начало статьи (предварительный просмотр) длиной 124 символа
#        и добавляет многоточие в конце.
class Bulletin(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)

    def preview(self):
        return self.body[:124] + '...'

    def get_replies(self):
        result = []
        for reply in Reply.objects.filter(bulletin=self):
            result.append(reply)
        return reversed(result)

    def get_absolute_url(self):
        return f'/board/{self.pk}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился


#        Модель Reply. Отклик на объявление. Модель будет иметь следующие поля:
#           связь «один ко многим» с моделью Bulletin;
#           связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь,
#           необязательно автор);
#           текст отклика;
#           дата и время создания отклика;
#           статус принятия отклика.
class Reply(models.Model):
    reply = models.CharField(max_length=255)
    reply_time = models.DateTimeField(auto_now_add=True)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)


class RegCode(models.Model):
    user = models.CharField(max_length=256)
    code = models.CharField(max_length=10)