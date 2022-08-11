from .cart import Cart


# context_processors
# for access the cart globally on all website templates
# so you should insert
# 'cart.context_processors.cart' in the templates in the setting file
# for make it globally access on templates
# i used it in the shop/base.html file
def cart(request):
    return {'cart': Cart(request)}
