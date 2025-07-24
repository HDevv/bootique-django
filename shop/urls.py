from django.urls import path
from .views import ProductListView, ProductDetailView, CartView, AccountView, AddToCartView, RemoveFromCartView
from django.contrib.auth import views as auth_views
from .views import InscriptionView


urlpatterns = [
    path('', ProductListView.as_view(), name='home'),  

    # PRODUITS    
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    
    
    # GESTION PANIER 
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    
    # LOGIN
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path("signup/", InscriptionView.as_view(), name="signup"),
]
