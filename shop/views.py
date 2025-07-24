from django.views.generic import ListView, DetailView, TemplateView, FormView
from .forms import InscriptionForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import Product, Category, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404


# LOGIN
class InscriptionView(FormView):
    template_name = "registration/register.html"
    form_class = InscriptionForm
    success_url = reverse_lazy('product_list')  # Redirection après inscription

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Connexion auto
        return super().form_valid(form)

# Homepage / liste produits
class ProductListView(ListView):
    model = Product
    template_name = 'produits/product_list.html'
    context_object_name = 'produits'

    def get_queryset(self):
        qs = Product.objects.all()
        cat_id = self.request.GET.get('category')
        if cat_id:
            qs = qs.filter(category_id=cat_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected = self.request.GET.get('category')  # en str
        context['selected_category'] = selected
        context['categories'] = Category.objects.all()
        return context


# Détail 
class ProductDetailView(DetailView):
    model = Product
    template_name = 'produits/product_detail.html'
    context_object_name = 'produit'

# Panier
class CartView(TemplateView):
    template_name = 'cart.html'

    
class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'


# Afficher panier
class CartView(LoginRequiredMixin, View):
    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        total = sum(item.subtotal() for item in items)
        return render(request, 'shop/cart.html', {'items': items, 'total': total})


# Ajouter produit au panier
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            item.quantity += 1
        item.save()
        return redirect('cart')


# Suppr article du panier
class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.delete()
        return redirect('cart')