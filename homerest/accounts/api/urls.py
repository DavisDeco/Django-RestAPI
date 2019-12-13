
from django.conf.urls import url

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token # should go to accounts app

from .views import LoginAPIView, RegisterAPIView

urlpatterns = [
    # 
    url(r'^$', LoginAPIView.as_view()),
    # 
    url(r'^register', RegisterAPIView.as_view()),




    # obtain new token when registered username and password is correct
    url(r'^jwt/$', obtain_jwt_token),
    # refresh new token when registered username and password is correct
    url(r'^jwt/refresh/$', refresh_jwt_token),


]