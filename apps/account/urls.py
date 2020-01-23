from django.urls import path

from .views import *

app_name = 'account'

urlpatterns = [
    path(r'accounts', AccountView.as_view({'get': 'list', 'post': 'create'}), name='accounts'),
    path(r'accounts/<uuid:id>',
         AccountView.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='accounts-detail'
         ),

    path('check-family-name', CheckFamilyNameAvailability.as_view({'post': 'check'}), name='check_family_name'),
    path('my-account', GetAccountInfoView.as_view({'get': 'list'}), name='my_account'),

]
