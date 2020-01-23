from django.urls import path
from .views import *

app_name = 'number'

urlpatterns = [

    path(
        r'numbers',
        NumberView.as_view({'post': 'create',
                            'get': 'list'
                            }),
        name='numbers'
    ),

    path(
        r'numbers/<str:e164_id>',
        SingleNumberView.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='single_number'
    ),

    path(
        r'accounts/<uuid:id>/numbers',
        AccountNumberView.as_view({'post': 'create',
                                   'get': 'list'
                                   }),
        name='account_numbers'
    ),

    path(
        r'accountnumbers/<uuid:id>',
        SingleAccountNumberView.as_view({
            'get': 'retrieve'
        }),
        name='single_account_number'
    ),
    path(
        r'accountnumbers/<uuid:id>/lidb',
        AccountNumberLidbView.as_view({
            'put': 'update',
            'get': 'list'
        }),
        name='account_number_lidb'
    ),
    path(
        r'accountnumbers/<uuid:id>/e911',
        E911View.as_view({
            'put': 'update',
            'get': 'list'
        }),
        name='account_e911'
    ),

    path(
        r'manual-create-number',
        ManualCreateNumber.as_view({
            'post': 'create'
        }),
        name='manual_create_number'
    ),

]
