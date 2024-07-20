from rest_framework import status
from rest_framework.exceptions import APIException


class GenericAPIException(APIException):
    def __init__(self, default_detail, status_code=status.HTTP_400_BAD_REQUEST, **kwargs):
        self.default_detail = default_detail
        self.status_code = status_code
        super(GenericAPIException, self).__init__(**kwargs)