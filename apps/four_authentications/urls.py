from django.urls import path

from .views import *

app_name = 'four_authentications'

urlpatterns = [
    path('signup', OktaSignup.as_view({'post': 'create'}), name='signup'),
    path('signin', OktaSignin.as_view({'post': 'create'}), name='signin'),
    path('signout', OktaLogout.as_view({'delete': 'destroy'}), name='logout'),
    path('active-account/<str:userid>', ActivateUserAccount.as_view({'post': 'create'}), name='activate_account'),

    path('forget-password', ForgetPassword.as_view({'post': 'create'}), name='forget_password'),
    path('reset-password', ResetPassword.as_view({'post': 'create'}), name='reset_password'),
]
