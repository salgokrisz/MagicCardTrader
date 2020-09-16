from django.urls import path, re_path
from . import views
from users import views as UsersView
from shopping_cart import views as CartView



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
    # /cards/add
    re_path(r'^cards/add/$', views.CardCreate.as_view(), name="card_add"),
    # cards/edit
    re_path(r'^cards/(?P<pk>[0-9]+)/edit/$', views.CardUpdate.as_view(), name="card_update"),
    # cards/delete
     re_path(r'^cards/(?P<pk>[0-9]+)/delete/$', views.CardDelete.as_view(), name="card_delete"),

    #/about/
    path('about/', views.about, name='about'),

    #re_path(r'^register/$', views.UserFormView.as_view(), name='register'),
    #/register, update_profile
    re_path(r'^profile/$', UsersView.profile, name="profile"),
    re_path(r'^register/$', UsersView.register, name="register"),
    re_path(r'^update_profile/$', UsersView.update_profile, name="update_profile"),

    #/cart urls
    re_path(r'add-to-cart/(?P<item_id>[-\w]+)/$', CartView.add_to_cart, name="add_to_cart"),
    re_path(r'^item/delete/(?P<item_id>[-\w]+)/$', CartView.delete_from_cart, name="delete_from_cart"),
    re_path(r'order-summary/', CartView.OrderSummaryView.as_view(), name="order_summary"),
    re_path(r'^checkout/$', CartView.CheckoutView.as_view(), name="checkout"),
    re_path(r'^payment/$', CartView.PaymentView.as_view(), name="payment"),
    #re_path(r'add-to-cart/<slug>/', CartView.add_to_cart, name="add_to_cart"),
    #re_path(r'^order-summary/$', CartView.order_details, name="order_summary"),
    #re_path(r'^checkout/$', CartView.checkout, name="checkout"),
    re_path(r'^success/$', CartView.success, name="purchase_success"),
    re_path(r'^update-transaction/(?P<order_id>[-\w]+)/$', CartView.update_transaction_records, name="update_records"),
    
]