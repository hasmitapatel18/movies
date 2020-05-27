from django.urls import path
from . import views
from movies_app.views import *




urlpatterns = [
    path('', FilmListView.as_view(), name='film_list'),

    path('film_detail/<int:pk>', views.FilmDetailView.as_view(), name='film_detail'),

    path('film/', views.FilmCreateView.as_view(), name='film_create'),

    path('movies_app/<int:pk>', views.FilmUpdateView.as_view(), name='film_update'),

    path('delete/<int:pk>', views.FilmDeleteView.as_view(), name='film_delete'),

    path('register/', views.RegisterView.as_view(), name='register'),

    path('film_detail/<int:pk>/comment/<int:comment_id>', views.CommentDeleteView.as_view(), name='comment_delete'),









]
