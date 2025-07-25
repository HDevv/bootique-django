from django.views.generic import ListView, DetailView, TemplateView, FormView
from .forms import InscriptionForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import Product, Category, CartItem, OrderItem, Order, Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator

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
    paginate_by = 20

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
        if self.request.user.is_authenticated:
            context['has_unread_notifications'] = Notification.objects.filter(
                user=self.request.user, is_read=False
            ).exists()
        return context


# Détail 
class ProductDetailView(DetailView):
    model = Product
    template_name = 'produits/product_detail.html'
    context_object_name = 'produit'

    
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
    
# PAIEMENT 
class PayOrderView(LoginRequiredMixin, View):
    def post(self, request):
        items = CartItem.objects.filter(user=request.user)
        if not items.exists():
            return redirect('cart')

        order = Order.objects.create(user=request.user, is_paid=True)

        # 👇 C’est ici que l'on doit bien créer les OrderItem
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price  
            )

        # Ensuite on peut vider le panier
        items.delete()

        return redirect('order_confirmation')
    
class OrderConfirmationView(TemplateView):
    template_name = "shop/order_confirmation.html"

# TABLEAU DE BORD 
@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "shop/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.paid()
        context['total_ca'] = Order.objects.total_ca()
        return context
    
# NOTIFS
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'shop/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')