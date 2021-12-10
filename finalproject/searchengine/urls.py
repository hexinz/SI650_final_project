from django.urls import path

from . import views
app_name = 'searchengine'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search),
    path('episode', views.episodeListView, name='list'),
    path(r'episode/<int:pk>&<int:rating>/rating',
         views.AddRating.as_view(), name='episode_rating'),
    path('episode/<int:pk>/unrating',
         views.DeleteRating.as_view(), name='episode_unrating'),
]