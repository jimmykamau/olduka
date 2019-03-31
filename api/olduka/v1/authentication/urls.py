from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

import olduka.v1.authentication.views.user_views as user_views

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('token/refresh/', refresh_jwt_token, name='refresh-token'),
    path('logout/', user_views.LogoutUserView.as_view(), name='logout'),
    path(
        'user/create/',
        user_views.CreateUserView.as_view(),
        name='create-user'
    ),
    path(
        'user/<slug:pk>/',
        user_views.RetrieveUpdateDestroyUserView.as_view(),
        name='user'
    )
]
