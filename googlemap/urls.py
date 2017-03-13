from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/update_tweets', views.update_tweets, name='update_tweets'),
    url(r'^ajax/stop_tweets', views.stop_tweets, name='stop_tweets'),
    url(r'^ajax/search', views.search, name='search'),
    url(r'^ajax/geosearch', views.geosearch, name='geosearch'),
    url(r'^ajax/first_fetch', views.first_fetch, name='first_fetch')
]
