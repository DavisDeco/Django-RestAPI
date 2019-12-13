
import json

from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
# import class based views  for rest-framework
# this enables us use class-based views rather than function based 
from rest_framework.views import APIView

from status.models import Status
from accounts.api.permissions import IsOwnerOrReadOnly

from .serializers import StatusSerializer


# using createModelMixin helps us to do a post and
# ListAPIView helps us list our resources after being created
class StatusAPIView( 
                    mixins.CreateModelMixin, 
                    generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #only authenticated users can access this resource
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    passed_id = None
    search_fields = ('user__username','context')
    ordering_fields = ('user__username','timestamp')

    # to override the ab ove queryset required parameter with a given argument
    # def get_queryset(self):
    #     request = self.request
    #     qs = Status.objects.all()
    #     query = request.GET.get('q')
    #     if query is not None:
    #         qs = qs.filter(context__icontains=query)
    #     return qs

    # post handled by CreateModelMixin
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    # 
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# using generic based class views
# class StatusCreateAPIView(generics.CreateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer

##################################################################################

# using generic based class views
class StatusDetailAPIView(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    # default look up is pk, but we can change it to 'id' or by using get_object() method below
    lookup_field = "id"

    # this method defines a custom lookup-field to search from objects (not necessary)
    # def get_object(self,*args,**kwargs):
    #     kwargs = self.kwargs
    #     kw_id = kwargs.get('id') # the get parameter can be any keyword eg slug,abc but be included in your url 
    #     return Status.objects.get(id=kw_id)

    # update handled by UpdateModelMixin
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    # patch handled by UpdateModelMixin
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    # delete handled by DestroyModelMixin
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)



# using generic based class views
# class StatusUpdateAPIView(generics.UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     # default look up is pk, but we can change it to 'id' or by using get_object() method below
#     lookup_field = "id"

# using generic based class views
# class StatusDeleteAPIView(generics.DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     # default look up is pk, but we can change it to 'id' or by using get_object() method below
#     lookup_field = "id"

#################################################################################
##################################################################################
################################## one api for all HTTP METHODS (not recommended but for practice) ##################

# # utility to show if data is json format
# def is_json(json_data):
#     try:
#         real_json = json.loads(json_data)
#         is_valid = True
#     except ValueError:
#         is_valid = False
#     return is_valid


# class StatusAPIView_V3( 
#                        mixins.CreateModelMixin,
#                        mixins.RetrieveModelMixin,
#                        mixins.UpdateModelMixin,
#                        mixins.DestroyModelMixin,
#                        generics.ListAPIView):
#     permission_classes = []
#     authentication_classes = []
#     # queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     passed_id = None

#     # to override the above queryset required parameter with a given argument
#     def get_queryset(self):
#         request = self.request
#         qs = Status.objects.all()
#         # get argument from a request for filter
#         query = request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(context__icontains=query)
#         return qs

#     # post handled by CreateModelMixin
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

    # enables us to override the default method
    # def get_object(self):
    #     request = self.request
    #     passed_id = request.GET.get('id',None) or self.passed_id 
    #     queryset = self.get_queryset()
    #     obj = None
    #     if passed_id is not None:
    #         obj = get_object_or_404(queryset,id=passed_id)
    #         self.check_object_permissions(request,obj)
    #     return obj

    # get handled by RetrieveModelMixin
    # def get(self,request,*args,**kwargs):
    #     url_passed_id = request.GET.get('id',None)

    #     json_data = {}
    #     body = request.body
    #     if is_json(body):
    #         json_data = json.loads(request.body)
    #     new_passed_id = json_data.get('id',None)
    #     # 
    #     passed_id = url_passed_id or new_passed_id or None
    #     self.passed_id = passed_id

    #     if passed_id is not None:
    #         return self.retrieve(request,*args,**kwargs)
    #     return super().get(request,*args,**kwargs) #this will call the get_object(self) above

    

    # # update handled by UpdateModelMixin
    # def put(self,request,*args,**kwargs):
    #     url_passed_id = request.GET.get('id',None)

    #     json_data = {}
    #     body = request.body
    #     if is_json(body):
    #         json_data = json.loads(request.body)
    #     new_passed_id = json_data.get('id',None)
    #     # 
    #     passed_id = url_passed_id or new_passed_id or None
    #     self.passed_id = passed_id
    #     return self.update(request,*args,**kwargs)

    # # patch handled by UpdateModelMixin
    # def patch(self,request,*args,**kwargs):
    #     url_passed_id = request.GET.get('id',None)

    #     json_data = {}
    #     body = request.body
    #     if is_json(body):
    #         json_data = json.loads(request.body)
    #     new_passed_id = json_data.get('id',None)
    #     # 
    #     passed_id = url_passed_id or new_passed_id or None
    #     self.passed_id = passed_id
    #     return self.update(request,*args,**kwargs)

    # # delete handled by DestroyModelMixin
    # def delete(self,request,*args,**kwargs):
    #     url_passed_id = request.GET.get('id',None)

    #     json_data = {}
    #     body = request.body
    #     if is_json(body):
    #         json_data = json.loads(request.body)
    #     new_passed_id = json_data.get('id',None)
    #     # 
    #     passed_id = url_passed_id or new_passed_id or None
    #     self.passed_id = passed_id
    #     return self.destroy(request,*args,**kwargs)
    
    # # 
    # def perform_destroy(self,instance):
    #     if instance is not None:
    #         return instance.delete()
    #     return None





##################################################################################
##################################################################################

# class StatusListSearchAPIView(APIView):
#     permission_classes = []
#     authentication_classes = []

#     # define HTTP request method
#     def get(self,request,format=None):
#         qs = Status.objects.all()
#         serializer = StatusSerializer(qs,many=True)
#         return Response(serializer.data)
#################################################################################
