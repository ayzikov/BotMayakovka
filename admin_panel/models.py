from django.db import models

class Piece(models.Model):
    name = models.TextField(verbose_name='Название пьесы')
    date = models.TextField(verbose_name='Дата выхода пьесы')
    genre = models.TextField(verbose_name='Жанр пьесы')
    description_piece = models.TextField(verbose_name='О пьесе')
    description_piece_detailed = models.TextField(verbose_name='Подробнее')
    description_play = models.TextField(verbose_name='О постановке')
    little_known = models.BooleanField(verbose_name='Малоизвестная пьеса')
    link_play = models.TextField(verbose_name='Ссылка на афишу')
    link_video = models.TextField(verbose_name='Ссылка на постановку в записи')
    image = models.ImageField(verbose_name='Изображение пьесы',
                              upload_to='images/',
                              blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пьеса'
        verbose_name_plural = 'Пьесы'


class User(models.Model):
    tg_id = models.IntegerField(verbose_name='id пользователя в телеграме')
    full_name = models.TextField(verbose_name='Имя пользователя')
    username = models.TextField(verbose_name='Юзернейм пользователя при наличии', default='')
    reg_time = models.DateTimeField(verbose_name='Дата регистрации пользователя')
    last_time = models.DateTimeField(verbose_name='Дата последнего действия пользователя')


class Action(models.Model):
    msg_id = models.IntegerField(verbose_name='id сообщения в телеграме')
    msg_name = models.TextField(verbose_name='Название выполненной команды')
    click_time = models.DateTimeField(verbose_name='время и дата выполненной команды')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь который совершил действие')