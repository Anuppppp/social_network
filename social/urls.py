from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchView, SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, ListFriendsView, ListPendingFriendRequestsView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friends/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friends/accept/<int:friend_request_id>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friends/reject/<int:friend_request_id>/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('friends/list/', ListFriendsView.as_view(), name='list-friends'),
    path('friends/pending/', ListPendingFriendRequestsView.as_view(), name='list-pending-friend-requests'),
]
