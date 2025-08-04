from django.urls import path
from . import views, feed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/<slug:category_slug>/', views.post_list, name='post_list_by_category'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('archive/<int:year>/<int:month>/', views.post_list, name='post_archive'),
    path('search/', views.post_list, name='post_search'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    path('post/<slug:slug>/dislike/', views.dislike_post, name='dislike_post'),
    path('rss/feed/', feed.LatestPostsFeed(), name='post_feed'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('author/panel/', views.author_panel, name='author_panel'),
    path('author/<str:username>/', views.author_profile, name='author_profile'),
    path('author/<str:username>/', views.AuthorProfileView.as_view(), name='author_profile'),
]
