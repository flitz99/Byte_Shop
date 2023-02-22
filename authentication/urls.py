from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('signout', views.signout, name='admin_signout'),
    path('<str:user_type>/signup',views.signup,name="signup"),
    path('<str:user_type>/signin',views.signin,name="signin"),
    path('users',views.users,name="users"),
    path('delete_user/<str:user_id>',views.delete_user,name="delete_user"),
    path('profile',views.profile,name="profile"),
    path('profile/change_password',views.change_password,name="change_password")
]
