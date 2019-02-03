from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('new_recruitment/', views.RecruitmentCreateView.as_view(), name='new_recruitment'),
    path('recruitment/<int:recruitment_id>/', views.RecruitmentDetailView.as_view(), name='recruitment_detail'),
    path('recruitment/<int:recruitment_id>/new_comment', views.RecruitmentCommentView.as_view(), name='new_comment'),
    path('recruitment/edit/<int:recruitment_id>/', views.RecruitmentEditView.as_view(), name='edit_recruitment'),
    path('message/<username>', views.MessageView.as_view(), name='message'),
    path('mypage', views.MyPageView.as_view(), name='mypage'),
    path('mypage/recruitment_list/', views.MyRecruitmentListView.as_view(), name='recruitment_list'),
    path('mypage/message_list/', views.MyMessageListView.as_view(), name='message_list'),
    path('mypage/profile/', views.MyProfileView.as_view(), name='show_profile'),
    path('mypage/config_profile/', views.ConfigProfileView.as_view(), name='config_profile'),
    path('mypage/edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('mypage/message/<int:message_id>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('mypage/message/reply/<str:sending_username>/', views.MessageReplyView.as_view(), name='message_reply'),
    path('mypage/recruitment/<int:recruitment_id>/delete/', views.RecruitmentDeleteView.as_view(), name='recruitment_delete'),
    path('mypage/footprint/', views.FootPrintView.as_view(), name='footprint'),
    path('<username>/', views.UserDetailView.as_view(), name='user_detail'),
]
