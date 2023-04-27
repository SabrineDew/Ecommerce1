from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from store.models import Product, Cart, Order


def index(request):

    products = Product.objects.all()
    return render(request, 'store/index.html', context={"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request,'store/detail.html', context={"product": product})

def add_to_cart(request,slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    #on recupére le produit s'il existe, sinon 404
    cart, _ = Cart.objects.get_or_create(user=user)
    # _ est mis parce qu'on utilise pas de variable, par convention pour celui qui relis le code
    #si le panier existe on le recupere, si pas on le crée
    order, created = Order.objects.get_or_create(user=user,ordered=False,product=product)
    #on verifier l'Order associé à l'utilisateur et qui correspond au produit ajouté


    if created:
        cart.orders.add(order)
        cart.save()
        #si le  produit vient d'etre crée on l'ajoute dans le panier et on enregistre celui-ci
    else:
        order.quantity += 1
        order.save()
        #si le produit etait deja dans le panier on incrémente sa quantité et on sauvegarde
        #c'est l'order qui doit etre incrementé pas le panier!

    return redirect(reverse("product", kwargs={"slug": slug}))

def cart(request):
    cart= get_object_or_404(Cart, user=request.user)
    return render(request, 'store/cart.html', context={"orders": cart.orders.all()})



def delete_cart(request):
    cart = request.user.cart
    if cart:
        cart.delete()
    return redirect('index')