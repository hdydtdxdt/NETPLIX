from django.urls import path

from .views import base_views, movie_views, recommend_views

app_name = 'watcha'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('movie/vote/<int:movie_id>/', movie_views.movie_vote, name='movie_vote'),
    path('recommend/', recommend_views.movie_display, name='recommend'),

    # # question_views.py
    # path('question/create/',
    #      question_views.question_create, name='question_create'),
    # path('question/modify/<int:question_id>/',
    #      question_views.question_modify, name='question_modify'),
    # path('question/delete/<int:question_id>/',
    #      question_views.question_delete, name='question_delete'),
    #
    # # answer_views.py
    # path('answer/create/<int:question_id>/',
    #      answer_views.answer_create, name='answer_create'),
    # path('answer/modify/<int:answer_id>/',
    #      answer_views.answer_modify, name='answer_modify'),
    # path('answer/delete/<int:answer_id>/',
    #      answer_views.answer_delete, name='answer_delete'),
    ]