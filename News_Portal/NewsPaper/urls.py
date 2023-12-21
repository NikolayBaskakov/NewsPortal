from django.urls import path
from .views import *
urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('articles/', ArticleList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/search/', post_search),
    path('articles/search/', post_search),
    path('news/create/', NewsCreate.as_view()),
    path('articles/create/', ArticlesCreate.as_view()),
    path('news/<int:pk>/edit/', NewsEdit.as_view()),
    path('articles/<int:pk>/edit/', ArticlesEdit.as_view()),
    path('news/<int:pk>/delete', NewsDelete.as_view()),
    path('articles/<int:pk>/delete', ArticlesDelete.as_view()),
    path('subscriptions/', subscriptions, name='subcriptions'),
    
]
