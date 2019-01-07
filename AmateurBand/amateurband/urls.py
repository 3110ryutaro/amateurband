from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mypage/new_recruitment/', views.RecruitmentView.as_view(), name='new_recruitment'),
    path('recruitment_list/', views.RecruitmentListView.as_view(), name='recruitment_list'),
    path('recruitment/<int:recruitment_id>/', views.RecruitmentDetailView.as_view(), name='recruitment_detail'),
    path('mypage', views.MyPageView.as_view(), name='mypage'),
    path('mypage/entry/', views.EntryView.as_view(), name='entry'),
    # path('article/', views.ArticleView.as_view(), name='article'),
    path('mypage/profile/', views.ProfileView.as_view(), name='profile'),
    # path('mypage/articles/edit/<int:article_id>/', views.ArticleEditView.as_view(), name='edit'),
    # path('mypage/articles/<int:article_id>/delete/', views.ArticleDeleteView.as_view(), name='delete'),
    path('mypage/message/', views.MessageView.as_view(), name='message_list'),
]
