from django.urls import path , include ,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from allauth.account.views import ConfirmEmailView 
from .views import ProfileView , CustomRegisterView ,CustomConfirmEmailView ,CustomGoogleLogin

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('accounts/', include('allauth.urls')),
    path('auth/profile/', ProfileView.as_view(), name='profile'),

    path('dj-rest-auth/google/', CustomGoogleLogin.as_view(), name='google_login'),


    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
            CustomConfirmEmailView.as_view(),
            name='account_confirm_email'),
]