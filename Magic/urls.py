from django.urls import path, re_path
from . import views

urlpatterns = [
    # /home/
    path('', views.index, name='MCTHome'),

    # /users/
    path('users/', views.users, name="MCT Users"),
    # /users/123/
    re_path(r'^users/(?P<user_id>[0-9]+)/$',views.user, name="user"),

    #/about/
    path('about/', views.about, name='MCT About'),
]