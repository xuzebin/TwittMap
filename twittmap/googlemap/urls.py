from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/update_tweets', views.update_tweets, name='update_tweets'),
    url(r'^ajax/stop_tweets', views.stop_tweets, name='stop_tweets'),
    url(r'^ajax/search', views.search, name='search')
]
