from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from allauth.account.views import SignupView, ConfirmEmailView

urlpatterns = [
    path('register/', views.register, name = 'user-register'),
    path('login/', views.login_page, name = 'user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name = 'user-logout'),
    path('profile/', auth_views.LoginView.as_view(template_name = 'user/profile.html'), name = 'user-profile'),
    path('profile/update/', views.profile_update, name = 'user-profile-update'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'user/password-reset.html'), name = 'password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'user/password-reset-done.html'), name = 'password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'user/password-reset-confirm.html'), name = 'password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'user/password-reset-complete.html'), name ='password_reset_complete'),
    path('confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='user_confirm_email'),
]