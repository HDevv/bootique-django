from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F, DecimalField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(blank=True, null=True)  # Image en URL
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    

class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"


class OrderQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(is_paid=True)

    def total_ca(self):
        return self.paid().aggregate(
            total=Sum(F('order_items__quantity') * F('order_items__price'), output_field=DecimalField())
        )['total'] or 0


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def paid(self):
        return self.get_queryset().paid()

    def total_ca(self):
        return self.get_queryset().total_ca()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    objects = OrderManager()

    @property
    def total(self):
        return sum(item.subtotal() for item in self.order_items.all())

    def __str__(self):
        return f"Commande #{self.id} de {self.user.username}"

# NOTIFS 
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif for {self.user.username} - {self.message[:20]}"
