
from rest_framework import pagination

# custom pagination
class CustomPagination(pagination.LimitOffsetPagination):    # PageNumberPagination):
    # page_size = 5
    default_limit = 3
    max_limit = 20
  