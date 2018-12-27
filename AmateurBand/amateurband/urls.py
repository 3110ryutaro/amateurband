from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/', views.ArticleView.as_view(), name='article'),
    path('mypage/profile/', views.ProfileView.as_view(), name='profile'),
    path('mypage/<int:user_id>/', views.MyPageView.as_view(), name='mypage'),
    path('mypage/articles/', views.ArticleListView.as_view(), name='article_list'),
    path('mypage/articles/<int:article_id>/', views.ArticleDetailView.as_view(), name='detail'),
    path('mypage/articles/<int:article_id>/edit/', views.ArticleEditView.as_view(), name='edit'),
    path('mypage/articles/<int:article_id>/delete/', views.ArticleDeleteView.as_view(), name='delete'),
    path('mypage/message/', views.MessageView.as_view(), name='message_list'),
    path('mypqge/recruitment/', views.RecruitmentView.as_view(), name='recruitment')
]