from rest_framework import viewsets, authentication,exceptions
from django.conf import settings

class Authentication(authentication.BasicAuthentication):

    def authenticate(self, request):
        api_token = request.META.get('HTTP_API_TOKEN')
        if not api_token:
            raise exceptions.AuthenticationFailed("Authorization header missing",
                                                  401)
        if api_token in settings.API_TOKEN:
            return True,None
        else:
            raise exceptions.AuthenticationFailed(" Authentication Failed :: Invalid  API Token.",
                                                  401)


class AuthBaseViewSet(viewsets.GenericViewSet):
    authentication_classes = [Authentication]
