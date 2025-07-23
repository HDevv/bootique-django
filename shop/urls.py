from django.urls import path
from .views import ProductListView, ProductDetailView, CartView, AccountView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),      
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cart/', CartView.as_view(), name='cart'), 
    path('account/', AccountView.as_view(), name='account'),
]
