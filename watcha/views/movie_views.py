from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url

from ..models import Movie


@login_required(login_url='common:login')
def movie_vote(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.voter.add(request.user)
    return redirect('{}#movie_{}'.format(resolve_url('watcha:index'), movie.id))