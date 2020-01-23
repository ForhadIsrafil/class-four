from django.urls import path
from .views import *
import django
from django.conf import settings
from django.conf.urls import url

app_name = 'order'

urlpatterns = [
    path(
        r'accounts/<uuid:id>/ordernumbers',
        OrderNumberView.as_view({'post': 'create'}),
        name='order_number'
    ),
    path(
        r'ordernumbers/<int:id>',
        SingleOrderNumberView.as_view({'get': 'retrieve'}),
        name='single_ordernumber'
    ),
    path(
        r'orders',
        AllOrderView.as_view({'get': 'list'}),
        name='all_orders'
    ),
    path(
        r'orders/<uuid:id>',
        SingleOrderView.as_view({'get': 'retrieve'}),
        name='single_order'
    ),
    path(
        r'accounts/<uuid:id>/orders',
        SingleAccountOrderView.as_view({'get': 'list'}),
        name='single_account_orders'
    ),
    path(r'orders/<uuid:id>/comments',
         OrderCommentView.as_view({'post': 'create',
                                   'get': 'list'}),
         name='order_comments'
         ),

    path(
        'orders/<uuid:id>/files',
         OrderFileView.as_view({'post': 'create',
                                'get': 'list'}),
         name='order_files'
         ),

    path(
        'orderfiles/<uuid:id>',
         SingelOrderFileView.as_view({'get': 'retrieve'}),
         name='single_order_file'
         ),
    path(
        'accounts/<uuid:id>/orderports',
        OrderPortView.as_view({'post': 'create'}),
         name='order_port'
         ),
    path('available-numbers', BandwidthAvailableNumbersView.as_view({'post': 'create'}),
         name='bandwidth_available_numbers'),


    url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),

]
