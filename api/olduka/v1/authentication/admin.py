from django.contrib import admin
import olduka.v1.authentication.models as authentication_models

admin.site.register(authentication_models.UserProfile)
