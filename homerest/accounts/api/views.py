from django.contrib.auth import authenticate, get_user_model
from django.db.models import  Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,permissions
from rest_framework_jwt.settings import api_settings

from .serializers import UserRegisterSerializer
from .permissions import AnonPermissionOnly

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER



User = get_user_model()

# register users using serializer(recommended approach)
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly] #we use our custom permission
    # permission_classes = [permissions.AllowAny]

    # method to pass request context to the serializer from this view
    def get_serializer_context(self,*args,**kwargs):
        return {"request": self.request}

# manually authenticate users (AuthAPIView)
class LoginAPIView(APIView):
    permission_classes = [AnonPermissionOnly] #we use our custom permission
    # permission_classes = [permissions.AllowAny]

    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            return Response({'detail': 'You are already authenticated'},status=400)
        # else get user data and authenticate
        data = request.data
        username = data.get('username')
        password = data.get('password')
        # 
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
            ).distinct()
        if qs.count() == 1:
            # print(qs.first())
            user_obj = qs.first()

            if user_obj.check_password(password):
                user = user_obj          
                # create user's payload token
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                # create response to return to user
                response = jwt_response_payload_handler(token,user,request=request)

                return Response(response)
        return Response({"detail": "Invalid credentials, please try again"}, status=401)


    
# manually Register/create new users (approach two, recommend using a serializer instead)
# class RegisterAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self,request,*args,**kwargs):
#         if request.user.is_authenticated():
#             return Response({'detail': 'You are already registered and authenticated'},status=400)
#         # else get user data and authenticate
#         data = request.data
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         password2 = data.get('password2')
#         # 
#         qs = User.objects.filter(
#             Q(username__iexact=username) |
#             Q(email__iexact=username) |
#             Q(email__iexact=email)
#             )
#         if password != password2:
#             return Response({"detail": "Passwords must match each other"}, status=401)
#         if qs.exists():
#             return Response({"detail": "This user already exists, please use different email"}, status=401)
#         else:
#             user = User.objects.create(username=username,email=email)
#             user.set_password(password)
#             user.save()
#             # create user's payload token
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             # create response to return to user
#             response = jwt_response_payload_handler(token,user,request=request)

#             return Response(response)            
               
#         return Response({"detail": "Invalid Request"}, status=400)