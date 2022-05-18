#!/usr/bin/env python
# coding: utf-8

# In[ ]:


WWW-Authenticate: Basic realm="api"


# In[ ]:


INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]


# In[ ]:


pip install djangorestframework


# In[4]:


from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)


# In[10]:


pip install django


# In[5]:


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# In[9]:


from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)


# In[11]:


from rest_framework.authtoken import views
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]


# In[ ]:


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# In[ ]:


urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]


# In[ ]:


from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


# In[ ]:




