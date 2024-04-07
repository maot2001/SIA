from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('search/', views.search, name='search'),
    path('recomm/', views.recomm, name='recomm'),
    path('movie/', views.movie, name='movie'),
    path('search/movie/', views.movie, name='movie'),
    path('recomm/movie/', views.movie, name='movie'),
    path('movie/<int:id>/', views.movie_id, name='movie_id'),
    path('movie/<int:id>/ping/', views.ping, name='ping'),
    path('save_duration/', views.save_duration, name='save_duration'),
    path('search/save_duration/', views.save_duration, name='save_duration'),
    path('recomm/save_duration/', views.save_duration, name='save_duration')
]
