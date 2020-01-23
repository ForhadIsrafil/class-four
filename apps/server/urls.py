from django.urls import path
from .views import ServerView, SingleServerView, RouteView, SingleRouteView, AllServerView

app_name = 'server'

urlpatterns = [
    path(
        r'accounts/<uuid:id>/routes',
        RouteView.as_view({
            'post': 'create',
            'get': 'list',
        }),
        name='routes'
    ),
    path(
        r'routes/<int:id>',
        SingleRouteView.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='routes'
    ),

    path(
        r'servers',
        AllServerView.as_view({
            'get': 'list',

        }),
        name='route_servers'
    ),
    path(
        r'routes/<int:id>/servers',
        ServerView.as_view({
                            'post': 'create',
                            'get': 'list',

                            }),
        name='route_servers'
    ),

    path(
        r'servers/<int:id>',
        SingleServerView.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='single_server'
    ),

]
