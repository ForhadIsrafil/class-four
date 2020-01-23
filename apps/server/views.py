from apps.decorators.permission_decorators import require_permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status
from .models import Server, Route
from .serializers import ServerSerializer, RouteSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import parsers, renderers, status
import json
from django.db import transaction
# from account.utils import slicer
from account.models import Account, AccountServer
from django.shortcuts import get_object_or_404
from apps.lib.views import ViewSet
from apps.lib.utils import get_pagination, slicer
from django.conf import settings


class RouteView(ViewSet):
    serializer_class = RouteSerializer

    # create routes with account id, if account id is valid
    @transaction.atomic
    @require_permissions(model=Account)
    def create(self, request, id):
        account = self.get_object_or_404(Account, id)

        request.data._mutable = True
        request.data['account'] = account

        serializer = RouteSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # show lists of routes for a single Account id with pagination
    @require_permissions(model=Account)
    def get_queryset(self):
        id = self.kwargs.get('id')
        account = self.get_object_or_404(Account, id)
        request = self.request
        routes = Route.objects.filter(account=account).order_by('-pk')
        return routes

    def get_serializer_context(self):
        return {'request': self.request}


class SingleRouteView(ViewSet):

    # retrieve serialized single data, based on route valid id
    def retrieve(self, request, id, format=None):
        route = self.get_object_or_404(Route, id)
        serializer = RouteSerializer(route, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # updating serialized single data, based on route valid id
    def partial_update(self, request, id):
        instance = self.get_object_or_404(Route, id)
        serializer = RouteSerializer(instance,
                                     data=request.data,
                                     partial=True,
                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete single route by route id
    @transaction.atomic
    def destroy(self, request, id):
        instance = self.get_object_or_404(Route, id)

        instance.server_set.all().delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllServerView(ViewSet):
    serializer_class = ServerSerializer

    # showing paginated lists of data of server
    def get_queryset(self):
        servers = Server.objects.filter(enabled=True).order_by('-pk')
        return servers

    def get_serializer_context(self):
        return {'request': self.request}


class ServerView(ViewSet):
    serializer_class = ServerSerializer

    # create server using by route valid id
    def create(self, request, id):

        route = self.get_object_or_404(Route, id)

        request.data._mutable = True
        request.data['route'] = route

        serializer = ServerSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # representing paginated all Server serialized data(informations) using by requested route id
    def get_queryset(self):
        id = self.kwargs.get('id')
        route = self.get_object_or_404(Route, id)
        servers = route.server_set.filter(enabled=True).order_by('-pk')
        return servers

    def get_serializer_context(self):
        return {'request': self.request}


class SingleServerView(ViewSet):

    # retrieve single represention of servers data(informations) using Server id
    def retrieve(self, request, id, format=None):
        server = self.get_object_or_404(Server, id)
        serializer = ServerSerializer(server, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # patch(updating) single Server informations by server id
    def partial_update(self, request, id):
        instance = self.get_object_or_404(Server, id)
        serializer = ServerSerializer(instance,
                                      data=request.data,
                                      partial=True,
                                      context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete single server, request of Server id
    @transaction.atomic
    def destroy(self, request, id):
        instance = self.get_object_or_404(Server, id)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
