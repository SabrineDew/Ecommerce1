from django.db import models
from django.urls import reverse
from django.utils import timezone

from shop.settings import AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(0.0)
    stock = models.IntegerField(0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}({self.stock})"

    def get_absolute_url(self):
        return reverse("product",kwargs={"slug": self.slug})


#Article (Order)

"""
- utilisateur
- produit
- quantité
- commandé ou non
"""

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # relation plusieur à 1, on va avoir plusieur article relié à un user(Foreignkey)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def get_total(self):
        total = self.product.price * self.quantity
        return total



#Panier(Cart)

"""
-utilisateur
-articles
-commandé ou non
-date de la commande
"""
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    #un user (utilisateur) ne peut avoir qu'un seul panier!! (onetoonefield) sinon on peut faire un foreignKey mais bien parametrer pour qu'il n'y a qu'un seul panier dans ce cas ci: models.ForeignKey(unique=True)
    orders= models.ManyToManyField(Order)



    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()

        super().delete(*args, **kwargs)