from django.contrib.auth import get_user_model
from rest_framework import generics,permissions,pagination


from accounts.api.permissions import AnonPermissionOnly
from status.api.serializers import StatusInlineUserSerializer
from status.models import Status
from status.api.views import StatusAPIView
from rest_framework.response import Response

from .serializers import UserDetailSerializer




User = get_user_model()

# Retrieve and Display details of a registered user
class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'username'

    # send context request to serializer
    def get_serializer_context(self):
        return {'request':self.request}



# Retrieve and Display status related registered user
# class UserStatusAPIView(generics.ListAPIView):
#     serializer_class = StatusInlineUserSerializer
#     search_fields = ('user__username','context')
#     # pagination_class = pagination.PageNumberPagination #inbuilt pagination

#     def get_queryset(self,*args,**kwargs):
#         # get username parameter from the url for filtering
#         username = self.kwargs.get("username",None)
#         if username is None:
#             return Status.objects.none()
#         return Status.objects.filter(user__username=username)


# Retrieve and Display status related registered user using StatusAPIView
class UserStatusAPIView(StatusAPIView):
    serializer_class = StatusInlineUserSerializer
    # search_fields = ('user__username','context')
    # pagination_class = pagination.PageNumberPagination #inbuilt pagination

    def get_queryset(self,*args,**kwargs):
        # get username parameter from the url for filtering
        username = self.kwargs.get("username",None)
        if username is None:
            return Status.objects.none()
        return Status.objects.filter(user__username=username)

    # over-ride the post method that is injected by StatusAPIView
    def post(self,request,*args,**kwargs):
        return Response({"detail":"Action not allowed here"}, status=400)

