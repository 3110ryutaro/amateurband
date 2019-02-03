from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('new_recruitment/', views.RecruitmentCreateView.as_view(), name='new_recruitment'),
    path('recruitment_list/', views.RecruitmentListView.as_view(), name='recruitment_list'),
    path('recruitment/<int:recruitment_id>/', views.RecruitmentDetailView.as_view(), name='recruitment_detail'),
    path('recruitment/<int:recruitment_id>/new_comment', views.RecruitmentCommentView.as_view(), name='new_comment'),
    path('recruitment/edit/<int:recruitment_id>/', views.RecruitmentEditView.as_view(), name='edit_recruitment'),
    path('recruitment/<int:recruitment_id>/message/', views.MessageView.as_view(), name='message'),
    path('mypage', views.MyPageView.as_view(), name='mypage'),
    path('mypage/config_profile/', views.ConfigProfileView.as_view(), name='config_profile'),
    path('mypage/message/<int:message_id>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('mypage/recruitment/<int:recruitment_id>/delete/', views.RecruitmentDeleteView.as_view(), name='recruitment_delete'),
]
