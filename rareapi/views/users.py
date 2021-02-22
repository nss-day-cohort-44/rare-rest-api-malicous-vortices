from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUser, Category, PostReaction, Reaction
from datetime import date
from django.contrib.auth.models import User


class Users(ViewSet):
    """Users"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single User
        Returns:
            Response -- JSON serialized User instance
        """

    def update(self, request, pk=None):
        """Handle PUT requests for a User
        Returns:
            Response -- Empty body with 204 status code
        """

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single User
        Returns:
            Response -- 200, 404, or 500 status code
        """

    def list(self, request):
        """Handle GET requests to /users resource
        Returns:
            Response -- JSON serialized list of Users
        """
        # Get all Post records from the database
        rare_user = RareUser.objects.get(user=request.auth.user)

        if rare_user.user.is_staff:
            rare_users = RareUser.objects.all()

            serializer = RareUserSerializer(
                rare_users, many=True, context={'request': request})
            return Response(serializer.data)

        else:
            return Response({'message': "This User does not have admin privileges."}, status=status.HTTP_401_UNAUTHORIZED)
            # Support filtering Users by type
            #    http://localhost:8000/Users?type=1
            #
            # That URL will retrieve all tabletop Users


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users
    Arguments:
        serializer type
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff')


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers
    Arguments:
        serializer type
    """
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'active')
        depth = 1
