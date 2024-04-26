from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model


class RemoteSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        session_id = request.META.get('HTTP_SESSIONID')
        if request.COOKIES.get('sessionid'):
            session_id = request.COOKIES.get('sessionid')

        if session_id:
            try:
                session = Session.objects.get(session_key=session_id)
                user_id = session.get_decoded().get('_auth_user_id')
                user = get_user_model().objects.get(pk=user_id)

                return (user, None)
            except (Session.DoesNotExist, KeyError, get_user_model().DoesNotExist):

                raise AuthenticationFailed('Invalid session')
        else:

            return None
