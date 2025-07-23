from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin

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