from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('recruit_entry/', views.RecruitEntryChoiceView.as_view(), name='recruit_entry'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/<int:kind>/', views.SignUpView.as_view(), name='kind_signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]