import http

from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
import random
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.forms.models import model_to_dict
from rest_framework import generics
from django.db.models import Q

# Create your views here.

#тут у нас будут сериалайзеры
class WordSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.Words
        fields = ['pk', 'word', 'translation_base']

class WordAPIView(generics.ListAPIView):
    queryset = models.Words.objects.all()
    serializer_class = WordSerializator

    def get(self, request):
        return Response({'word': 'Cat'})

    def post(self, request):
        word = models.Words.objects.create(
            word=request.data['word'],
            translation_base=request.data['translation_base']
        )
        return Response({'post': model_to_dict(word)})


#Создадим вью, которое будет приминать запрос пользователя и
#отдавать случайное слово, сериализованное, т.е. пригодное
#для передачи по REST API
class RandomWord(APIView):
    #переопределяем медод get
    def get(self, *args, **kwargs):

        random4traslations = []
        all_words = models.Words.objects.all()  #получаем все слова из БД
        word = random.choice(all_words)

        for i in range(4):
            all_words = models.Words.objects.all()
            random_trt = random.choice(all_words)
            random4traslations.append(random_trt.translation_base)

        #serialized_random_word = WordSerializator(random_word, many=False)
        #return Response(serialized_random_word.data)

        return Response({
            'status': 0,
            'msg': 'Вот набор слов',
            'word': word.word,
            'translation_base': word.translation_base,
            'random_trt': random4traslations
        })




#Создадим вью, которое будет приминать запрос пользователя и
#отдавать следующее слово, сериализованное, т.е. пригодное
#для передачи по REST API
class NextWord(APIView):
    def get(self, request, pk, format=None):
        word = models.Words.objects.filter(pk__gt=pk).first()
        if not word:
            return HttpResponseNotFound()
        serialized_word = WordSerializator(word, many=False)
        return Response(serialized_word.data)

class AddWord(APIView):
    #переопределяем медод post
    def post(self, request):
        #1 проверяем, есть ли такое слово в БД
        is_word = 1
        try:
            word = models.Words.objects.filter(Q(word=request.data['word'])).first()
            return Response({
                'status': 1,
                'msg': 'Такое слово уже существует!',
                'word': model_to_dict(word)["word"],
                'translation_base': model_to_dict(word)["translation_base"]
            })
        except:
            if request.data['translation_base'] != '':
                word = models.Words.objects.create(
                    word=request.data['word'],
                    translation_base=request.data['translation_base'],
                    user_id=request.data['user_id']
                )
                return Response({
                    'status': 0,
                    'msg': 'Слово успешно добавлено в словарь!',
                    'word': model_to_dict(word)["word"],
                    'translation_base': model_to_dict(word)["translation_base"]
                })
            else:
                return Response({
                    'status': 2,
                    'msg': 'Этого слова нет!',
                    'word': '',
                    'translation_base': ''
                })

class DeleteWord(APIView):
    def post(self, request):
        # 1 проверяем, есть ли такое слово в БД
        is_word = 1
        try:
            word = models.Words.objects.filter(Q(word__icontains=request.data['word'])).first()
            word.delete()
            return Response({
                'status': 1,
                'msg': 'Слово удалено!',
                'word': model_to_dict(word)["word"]
            })
        except:
            return Response({
                'status': 0,
                'msg': 'Произошла ошибка!'
            })


class UpdateWord(APIView):
    def post(self, request):
        #1 проверяем, есть ли такое слово в БД
        is_word = 1
        try:
            if request.data['word_edit'] !='':
                #
                #   Если прилетело редактирование самого слова
                #
                word = models.Words.objects.filter(Q(word=request.data['word'])).first()
                word.word = request.data['word_edit']
                word.save()
                word = models.Words.objects.filter(Q(word=request.data['word_edit'])).first()
                return Response({
                    'status': 1,
                    'msg': 'Слово исправлено!',
                    'word': model_to_dict(word)["word"],
                    'translation_base': model_to_dict(word)["translation_base"]})
            else:
                #
                #   Если прилетело редактирование перевода
                #
                word = models.Words.objects.filter(Q(word=request.data['word'])).first()
                word.translation_base = request.data['translation_edit']
                word.save()
                word = models.Words.objects.filter(Q(word=request.data['word'])).first()
                return Response({
                    'status': 2,
                    'msg': 'Перевод исправлен!',
                    'word': model_to_dict(word)["word"],
                    'translation_base': model_to_dict(word)["translation_base"]})
        except:
            return Response({
                'status': 3,
                'msg': 'Ищи ошибку',
                'word': '',
                'translation_base': ''})





