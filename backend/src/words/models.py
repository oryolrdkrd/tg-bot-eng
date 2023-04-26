from django.db import models

# Create your models here.

class Words(models.Model):
#Представляет собой класс, описывающий представление хранимых данных о слове

    #Описание рода слова
    GENDERS = [
        ('male', 'Мужской'),
        ('neuter', 'Средний'),
        ('female', 'Женский')
    ]

    word = models.CharField(verbose_name='Word', max_length=255)
    gender = models.CharField(verbose_name='Gender', max_length=6, choices=GENDERS)
    translation_base = models.CharField(verbose_name='Translation', max_length=255)
    user_id = models.CharField(verbose_name='User_ID', max_length=255)

    #базовый перевод слова, предполагается, что вариации будут храниться в другой таблице в будущем

    def __str__(self) -> str:
        return self.gender + " " + self.word + " " + self.translation_base