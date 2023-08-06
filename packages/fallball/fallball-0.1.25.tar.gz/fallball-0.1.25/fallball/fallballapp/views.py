from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fallballapp.models import Application, Client, ClientUser, Reseller
from fallballapp.serializers import (ApplicationSerializer, ClientSerializer,
                                     ClientUserSerializer, ResellerSerializer)
from fallballapp.utils import (dump_exits, get_all_reseller_clients,
                               get_all_resellers, get_app_username, get_object_or_403, repair)


class ApplicationViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.create(self, request, *args, **kwargs)
        return Response("Only superuser can create application", status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.list(self, request, *args, **kwargs)
        return Response("Authorization failed", status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.retrieve(self, request, *args, **kwargs)
        return Response("Authorization failed", status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.destroy(self, request, *args, **kwargs)
        return Response("Authorization failed", status=status.HTTP_403_FORBIDDEN)


class ResellerViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ResellerSerializer
    queryset = Reseller.objects.all()
    lookup_field = 'name'

    def create(self, request, *args, **kwargs):
        application = get_object_or_403(Application, owner=request.user)
        if application:
            request.data['application'] = application
            return ModelViewSet.create(self, request, *args, **kwargs)
        return Response("Reseller should be created with application token",
                        status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        application = get_object_or_403(Application, owner=request.user)
        if not application:
            return Response("Authorization failed", status=status.HTTP_403_FORBIDDEN)
        Reseller.objects.filter(name=kwargs['name'], application=application).delete()
        username = get_app_username(kwargs['name'], application.id)
        User.objects.filter(username=username).delete()
        return Response('Reseller has been deleted', status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        Method is overwritten in order to implement superuser check
        """
        application = get_object_or_403(Application, owner=request.user)
        if not application:
            return Response("Authorization failed", status=status.HTTP_403_FORBIDDEN)
        queryset = Reseller.objects.filter(application=application)
        serializer = ResellerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        application = get_object_or_403(Application, owner=request.user)
        reseller = get_object_or_404(Reseller, application=application, name=kwargs['name'])

        if not application:
            return Response("Authorization failed",
                            status=status.HTTP_403_FORBIDDEN)
        queryset = [reseller, ]
        serializer = ResellerSerializer(queryset, many=True)
        return Response(serializer.data[0])

    @detail_route(methods=['get'])
    def reset(self, request, *args, **kwargs):
        """
        Repair particular reseller
        """
        application = get_object_or_403(Application, owner=request.user)

        if application:
            reseller = get_object_or_404(Reseller, pk=kwargs['pk'])
        else:
            reseller = get_object_or_403(Reseller, pk=kwargs['pk'], owner=request.user)

        # Check if reseller exists in database
        if dump_exits(reseller.pk):
            repair(Reseller, reseller.pk)
            return Response("All clients has been repaired", status=status.HTTP_200_OK)
        return Response("This reseller cannot be repaired",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @list_route(methods=['get'])
    def reset_all(self, request, *args, **kwargs):
        """
        Repair particular reseller
        """
        application = get_object_or_403(Application, owner=request.user)

        if not application:
            return Response("Only superuser can repair all resellers",
                            status=status.HTTP_403_FORBIDDEN)
        # Delete all existed resellers prior to reparing:
        Reseller.objects.all().delete()

        # Get list of available resellers from dump and repair one by one
        resellers = get_all_resellers()
        for reseller in resellers:
            repair(Reseller, reseller['pk'])
        return Response("All resellers has been repaired", status=status.HTTP_200_OK)


class ClientViewSet(ModelViewSet):
    """
    ViewSet which manages clients
    """
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'name'

    def create(self, request, *args, **kwargs):
        """
        Create new reseller client
        """
        application = Application.objects.filter(owner=request.user).first()
        if application:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         application=application)
        else:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         owner=request.user)
        if not Client.objects.filter(reseller=reseller,
                                     name=request.data['name']):
            # Check if there is a free space for new client
            free_space = reseller.limit - reseller.get_usage()
            if free_space >= request.data['storage']['limit']:
                # Every client should belong to particular reseller
                request.data['reseller'] = reseller
                return ModelViewSet.create(self, request, *args, **kwargs)
            return Response("Reseller limit is reached", status=status.HTTP_400_BAD_REQUEST)
        return Response("Such client already exists", status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """
        Return list of clients which owned by particular reseller
        """
        # If application token is provided we just get reseller for this application from the db
        # If reseller token is provided we need to check that clients are owned by this reseller
        application = Application.objects.filter(owner=request.user).first()
        if application:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         application=application)
        else:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         owner=request.user)

        queryset = Client.objects.filter(reseller=reseller)
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Return particular client which owned by particular reseller
        """
        application = Application.objects.filter(owner=request.user).first()
        if application:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         application=application)
        else:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         owner=request.user)
        client = Client.objects.filter(reseller=reseller, name=kwargs['name'])
        if not client:
            return Response("Client does not exist", status=status.HTTP_404_NOT_FOUND)
        queryset = client
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data[0])

    def destroy(self, request, *args, **kwargs):
        application = Application.objects.filter(owner=request.user).first()
        if application:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         application=application)
        else:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         owner=request.user)
        client = Client.objects.filter(name=kwargs['name'], reseller=reseller).first()
        if client:
            client.delete()
            return Response('Client has been deleted', status=status.HTTP_204_NO_CONTENT)
        return Response('Such client does not exist', status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'])
    def reset(self, request, *args, **kwargs):
        """
        Recreate client to initial state
        """
        if request.user.is_superuser:
            reseller = get_object_or_403(Reseller, pk=kwargs['reseller_pk'])
        else:
            reseller = get_object_or_403(Reseller, pk=kwargs['reseller_pk'], owner=request.user)

        # Check that client belongs to particular reseller
        get_object_or_404(Client, reseller=reseller, pk=kwargs['pk'])
        try:
            repair(Client, kwargs['pk'])
        except:
            return Response("This client cannot be repaired",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("Client has been repaired", status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def reset_all(self, request, *args, **kwargs):
        """
        Recreate all reseller clients to initial state
        """
        if request.user.is_superuser:
            reseller = get_object_or_403(Reseller, pk=kwargs['reseller_pk'])
        else:
            reseller = get_object_or_403(Reseller, pk=kwargs['reseller_pk'], owner=request.user)

        clients = get_all_reseller_clients(kwargs['reseller_pk'])
        if not clients:
            return Response("There are no clients to repair",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Delete all reseller clients
        Client.objects.filter(reseller=reseller).delete()
        for client in clients:
            repair(Client, client['pk'])
        return Response("All clients has been repaired", status=status.HTTP_200_OK)


class ClientUserViewSet(ModelViewSet):
    """
    Create new client user
    """
    queryset = ClientUser.objects.all().order_by('-id')
    serializer_class = ClientUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'email'
    # Redefine regex in order to get user email as id
    lookup_value_regex = '[^@]+@[^@]+\.[^@]+'

    def create(self, request, *args, **kwargs):
        application = Application.objects.filter(owner=request.user).first()
        if application:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         application=application)
        else:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         owner=request.user)

        # get client to provide it for user creation
        client = Client.objects.filter(reseller=reseller,
                                       name=kwargs['client_name']).first()
        if not client:
            return Response("Authorization failed", status=status.HTTP_403_FORBIDDEN)

        # Check if client has free space for new user
        free_space = client.limit - client.get_usage()
        if free_space >= request.data['storage']['limit']:
            request.data['client'] = client
            request.data['application_id'] = reseller.application.id
            if 'admin' not in request.data:
                request.data['admin'] = False

            return ModelViewSet.create(self, request, *args, **kwargs)

        return Response("Client limit is reached", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        application = Application.objects.filter(owner=request.user).first()
        if application:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         application=application)
        else:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         owner=request.user)

        client_user = ClientUser.objects.filter(email=kwargs['email']).first()
        if client_user.client.reseller == reseller:
            client_user.delete()
            User.objects.filter(username='{}.{}'.format(reseller.application.id,
                                                        kwargs['email'])).delete()
            return Response("User has been deleted", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Authorization failed", status=status.HTTP_403_FORBIDDEN)

    def list(self, request, **kwargs):
        application = Application.objects.filter(owner=request.user).first()
        if application:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         application=application)
        else:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         owner=request.user)

        client = get_object_or_404(Client, reseller=reseller, name=kwargs['client_name'])
        queryset = ClientUser.objects.filter(client=client)
        serializer = ClientUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        application = Application.objects.filter(owner=request.user).first()
        if application:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         application=application)
        else:
            reseller = get_object_or_403(Reseller, name=kwargs['reseller_name'],
                                         owner=request.user)

        client = Client.objects.filter(reseller=reseller, name=kwargs['client_name'])
        client_user = ClientUser.objects.filter(client=client, email=kwargs['email'])
        if not client_user:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        queryset = client_user
        serializer = ClientUserSerializer(queryset, many=True)
        return Response(serializer.data[0])


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = ClientUser.objects.filter(user_id=request.user.id).first()
        serializer = ClientUserSerializer(queryset)
        return Response(serializer.data)
