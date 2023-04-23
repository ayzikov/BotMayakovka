from django.db import models

class Piece(models.Model):
    name = models.TextField(verbose_name='Название пьесы')
    date = models.TextField(verbose_name='Дата выхода пьесы')
    genre = models.TextField(verbose_name='Жанр пьесы')
    description_piece = models.TextField(verbose_name='О пьесе')
    description_piece_detailed = models.TextField(verbose_name='Подробнее')
    description_play = models.TextField(verbose_name='О постановке')
    little_known = models.BooleanField(verbose_name='Малоизвестная пьеса')
    image = models.ImageField(verbose_name='Изображение пьесы',
                              upload_to='images/',
                              blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пьеса'
        verbose_name_plural = 'Пьесы'
