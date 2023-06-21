from django.urls import path, include

from news.api import views

from rest_framework.authtoken import views as auth_views
# from news.api.custom_auth_view import CustomAuthToken


urlpatterns = [
    # function based
    # path('articles/', views.article_list_create_api_view, name='article-list'),
    # path('articles/<int:pk>', views.article_detail_api_view, name='article-detail'),

    # class based
    # path('articles/', views.ArticleListCreateAPIView.as_view(), name='article-list'),
    # path('articles/<int:pk>', views.ArticleDetailAPIView.as_view(), name='article-detail'),
    # path('authors/', views.JournalistListCreateAPIView.as_view(), name='author-list'),

    # generics
    path('authors/', views.JournalistList.as_view(), name='author-list'),
    path('authors/<int:pk>', views.JournalistDetail.as_view(), name='author-detail'),

    path('authors/<int:author_id>/addarticle', views.ArticleCreate.as_view(), name='article-create'),
    path('articles/', views.ArticleList.as_view(), name='article-list'),
    path('articles/<int:pk>', views.ArticleDetail.as_view(), name='article-detail'),

    path('articles/<int:article_id>/addcomment', views.CommentCreate.as_view(), name='comment-create'),
    path('comments/<int:pk>', views.CommentDetail.as_view(), name='comment-detail'),

    path('api-auth/', include('rest_framework.urls')),

    path('api-auth-token/', auth_views.obtain_auth_token),
    # path('api-auth-token/', CustomAuthToken.as_view()),

]
