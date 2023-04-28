from django.urls import path
from . import views

urlpatterns = [
    path('random/', views.RandomWord.as_view()),
    path('next/<int:pk>', views.NextWord.as_view()),
    path('addword/', views.AddWord.as_view()),
    path('updateword/', views.UpdateWord.as_view()),
    path('delword/', views.DeleteWord.as_view()),
    path('words/', views.WordAPIView.as_view()),
]