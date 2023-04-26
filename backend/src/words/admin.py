from django.contrib import admin

# Register your models here.
from . import models

#Определим класс, как будут представляться наши модели в
#списочном виде
class WordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'gender', 'word', 'translation_base', 'user_id']
    list_editable = ['gender', 'word', 'translation_base']

#Регистрация нашей модели на сайте админа
admin.site.register(models.Words, WordAdmin)