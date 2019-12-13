
from django.conf.urls import url

from .views import (
    # StatusListSearchAPIView,
    StatusAPIView,
    # StatusAPIView_V3,
    # StatusCreateAPIView,
    StatusDetailAPIView,
    # StatusUpdateAPIView,
    # StatusDeleteAPIView
    )

urlpatterns = [
    # url(r'^$',StatusListSearchAPIView.as_view()),
    url(r'^$',StatusAPIView.as_view()), # demo: other ways but same
    # this url demos all http methods from one endpoint
    # url(r'^v3/$',StatusAPIView_V3.as_view()),
    # url(r'^create/$',StatusCreateAPIView.as_view()),
    url(r'^(?P<id>\d+)',StatusDetailAPIView.as_view(), name='detail'),
    # url(r'^(?P<id>\d+)/update/$',StatusUpdateAPIView.as_view()),
    # url(r'^(?P<id>\d+)/delete/$',StatusDeleteAPIView.as_view()),


]
