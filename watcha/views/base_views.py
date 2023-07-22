from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Movie
import pandas as pd

data = pd.read_csv('./resources/data.csv', encoding='cp949')
for i in range(len(data)):
   m = Movie()
   m.title = data['title'][i]
   m.story = data['story'][i]
   m.url = data['url'][i]
   m.save()

def index(request):
    movie_list = Movie.objects.order_by('title')
    context = {'movie_list': movie_list}
    return render(request, 'watcha/movie_list.html', context)
