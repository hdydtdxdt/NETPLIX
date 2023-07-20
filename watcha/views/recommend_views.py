import itertools

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.db.models import Q

from ..models import Movie

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('./resources/data.csv', encoding='cp949')
first = int(len(data) / 3)
second = int(len(data) / 3 * 2)
third = int(len(data))
stopwords = []
stopwords_path = './resources/stopwords.txt'

with open(stopwords_path, 'r', encoding='utf-8') as stopwords_file:
    line = stopwords_file.readline()

    while True:
        line = stopwords_file.readline()
        if not line: break
        stopwords.append(line[:-1])

stopwords_file.close()

tfidf = TfidfVectorizer(stop_words=stopwords)
tfidf_matrix = tfidf.fit_transform(data['story'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def reset_order():
    movies = Movie.objects.all()
    for movie in movies:
        movie.order = -1
        movie.save()

def get_recommendations(title, cosine_sim=cosine_sim):
    title_to_index = dict(zip(data['title'], data.index))
    idx = title_to_index[title]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    similar_movie_scores = sim_scores[:first]
    similar_movie_indices = [idx[0] for idx in similar_movie_scores]

    return similar_movie_indices

def evaluate(request):
    user_movies = data.copy()
    for i in range(len(user_movies)):
        user_movies['score'] = 0

    reset_order()

    sorted_movies = []
    similar_movies = []
    opposite_movies = []

    titles = []

    user = request.user
    voted_movies = user.voter_movie.all()

    if len(voted_movies) == 0:
        return 0
    else:
        for i in range(len(voted_movies)):
            indexes = get_recommendations(voted_movies[i].title)
            for index in indexes:
                user_movies.loc[index, 'score'] += 10

        user_movies = user_movies.sort_values(by='score', ascending=False)
        user_movies = user_movies.reset_index(drop=True)

        for i in range(len(user_movies)):
            titles.append(user_movies.loc[i, 'title'])

        for i in range(second):
            similar_movies.append(titles[i])

        for i in range(second, third):
            opposite_movies.append(titles[i])

        j = 0
        k = 0
        while True:
            if j == 184:
                break
            sorted_movies.append(similar_movies[j:j + 8])
            sorted_movies.append(opposite_movies[k:k + 8])
            j += 8
            k += 2
        sorted_movies.append(similar_movies[j:186])
        sorted_movies.append(opposite_movies[k:k + 2])

        sorted_movies = list(itertools.chain(*sorted_movies))

        order = 1
        for sorted_title in sorted_movies:
            movies = Movie.objects.filter(title=sorted_title)
            for movie in movies:
                movie.order = order
                movie.save()
            order += 1

@login_required(login_url='common:login')
def movie_display(request):
    evaluate(request)
    movie_list = Movie.objects.filter(~Q(order=-1))
    movie_list = movie_list.order_by('order')
    context = {'movie_list': movie_list}
    return render(request, 'watcha/movie_recommend.html', context)
