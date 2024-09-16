
from django.urls import path
from .views import RegisteruserView,VerifyUserEmail,LoginUserView,PasswordResetConfirm,PasswordResetRequestView,SetNewPassword,LogoutUserView,TestAuthenticationView,get_user_details
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns=[
    path('register/',RegisteruserView.as_view(),name='register'),
    path('verify-email/',VerifyUserEmail.as_view(),name='verify'),
    path('login/',LoginUserView.as_view(),name='login'),
    path('password-reset/',PasswordResetRequestView.as_view(),name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirm.as_view(),name='password-reset-confirm'),
    path('set-new-password/',SetNewPassword.as_view(),name='set-new-password'),
    path('logout/',LogoutUserView.as_view(),name='logout'),
    # path('get-something/', TestAuthenticationView.as_view(), name='just-for-testing'),
    path('dashboard/',TestAuthenticationView.as_view(),name='granted'),
    path('token/refresh/',TokenRefreshView.as_view(),name='refresh-token'),
    path('user-details/', get_user_details, name='user-details'),
    
    
]
