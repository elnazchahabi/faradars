from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import WalletChargeView

urlpatterns = [
    # کل احراز هویت ایمیل/پسورد را بده به allauth:
    path('', include('allauth.urls')),

    # فقط OTP موبایل و پروفایل و داشبورد سفارشی نگه‌دار:
    path('signup/mobile/', views.mobile_signup_request, name='mobile_signup'),
    path('signup/otp/', views.otp_verify, name='otp_verify'),

    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    path('deactivate/', views.DeactivateAccountView.as_view(), name='deactivate_account'),
    path('instructor-request/', views.InstructorRequestView.as_view(), name='instructorrequest'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
    template_name='account/password_change.html'), name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
    template_name='account/password_change_done.html'), name='password_change_done'),

    path('support/', include('support.urls')),
    path('wallet/charge/', WalletChargeView.as_view(), name='wallet_charge'),

]






