from django.urls import include, path

import olduka.v1.authentication.views.user_views as user_views

urlpatterns = [
    path(
        'user/create/',
        user_views.CreateUserView.as_view(),
        name='create-user')
]
