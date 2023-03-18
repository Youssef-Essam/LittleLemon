from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [

    
    path('groups/manager/users/', views.managers),
    path('api-token-auth/', obtain_auth_token),
    path('cart/menu-items', views.CartView.as_view()),

    path('orders/<int:pk>', views.SingleMenuItemView.as_view()),
    path('order', views.OrderView.as_view()),
    
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-items', views.ManagerMenuItemView.as_view()),
    path('menu-items/<int:pk>', views.ManagerSingleMenuItemView.as_view()),
    
]
