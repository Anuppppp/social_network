from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, FriendRequest
from .serializers import CustomUserSerializer, UserSignupSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_ratelimit.decorators import ratelimit


class UserSignupView(APIView):
    """
    API endpoint for user registration.
    Allows users to sign up by providing their email, username, and password.
    """

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    API endpoint for user login.
    Users can log in using their email and password. The response includes JWT access and refresh tokens.
    """

    def post(self, request):
        email = request.data.get('email', '').lower()  # Ensures email is case-insensitive
        password = request.data.get('password', '')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserSearchView(APIView):
    """
    API endpoint for searching users by email or username.
    Only authenticated users can access this endpoint. Search is case-insensitive and supports pagination.
    """
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view

    class UserPagination(PageNumberPagination):
        page_size = 10

    def get(self, request):
        query = request.query_params.get('q', '').lower()  # Case-insensitive search
        if query:
            users = CustomUser.objects.filter(
                Q(email__iexact=query) | Q(username__icontains=query)
            )
            paginator = self.UserPagination()
            result_page = paginator.paginate_queryset(users, request)
            serializer = CustomUserSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)


class SendFriendRequestView(APIView):
    """
    API endpoint for sending friend requests.
    Users can send friend requests to other users by providing the receiver's ID. Rate-limited to 3 requests per minute.
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='3/m', block=True))
    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        try:
            receiver = CustomUser.objects.get(id=receiver_id)
            friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver,
                                                                          status='pending')
            if created:
                return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Friend request already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class AcceptFriendRequestView(APIView):
    """
    API endpoint for accepting friend requests.
    Users can accept friend requests directed to them. The friend request's status is changed to 'accepted'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_request_id):
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, receiver=request.user, status='pending')
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)


class RejectFriendRequestView(APIView):
    """
    API endpoint for rejecting friend requests.
    Users can reject friend requests directed to them, changing the request's status to 'rejected'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_request_id):
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, receiver=request.user)
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)


class ListFriendsView(APIView):
    """
    API endpoint for listing all friends.
    Lists all users who have an accepted friend request with the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = FriendRequest.objects.filter(
            (Q(sender=request.user) | Q(receiver=request.user)) & Q(status='accepted')
        )
        friends_list = [friend.sender if friend.receiver == request.user else friend.receiver for friend in friends]
        serializer = CustomUserSerializer(friends_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListPendingFriendRequestsView(APIView):
    """
    API endpoint for listing pending friend requests.
    Lists all pending friend requests directed to the logged-in user,
    optimizing query performance by pre-fetching senders.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending').select_related(
            'sender')
        serializer = CustomUserSerializer([req.sender for req in pending_requests], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
