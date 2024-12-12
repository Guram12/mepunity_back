from django.urls import path , include ,re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from allauth.account.views import ConfirmEmailView 
from .views import ProfileView , CustomRegisterView ,CustomConfirmEmailView ,CustomGoogleLogin , ProfileFinishView \
    , PasswordResetRequestView , PasswordResetConfirmView , ProfileUpdateView , CustomTokenObtainPairView 

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('accounts/', include('allauth.urls')),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path("auth/profile/complite/", ProfileFinishView.as_view(), name='profile_complite'),
    path('auth/profile/update/', ProfileUpdateView.as_view(), name='profile_update'),


    path('dj-rest-auth/google/', CustomGoogleLogin.as_view(), name='google_login'),

    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
            CustomConfirmEmailView.as_view(),
            name='account_confirm_email'),

    # password reset urls 
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]