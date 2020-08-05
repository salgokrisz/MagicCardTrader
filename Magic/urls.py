from django.urls import path, re_path
from . import views


app_name = 'Magic'
urlpatterns = [
    # /home/
    path('', views.index, name='index'),

    # /users/
    #path('users/', views.UsersView.as_view(), name="users"), #generic views
    #re_path(r'^users/(?P<pk>[0-9]+)/$',views.UserDetailView.as_view(), name="user_detail"), #generic views
    path('users/', views.users, name="users"),
    # /users/123/
    re_path(r'^users/(?P<user_id>[0-9]+)/$',views.user_detail, name="user_detail"),
    
    # /cards
    path('cards/', views.cards, name="cards"),
    # /cards/123
    re_path(r'^cards/(?P<card_id>[0-9]+)/$',views.card_detail, name="card_detail"),

    #/about/
    path('about/', views.about, name='about'),
]