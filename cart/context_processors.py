from .cart import Cart


# for access the cart globally on all website templates
def cart(request):
    return {'cart': Cart(request)}
