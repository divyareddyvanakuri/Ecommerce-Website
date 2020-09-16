from django.contrib.auth import get_user_model

class AuthBackend(object):
    def authenticate(self, request, username=None, phonenumber=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False):
                return user
        return None
    def get_user(self, user_id):
        User = get_user_model()        
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None