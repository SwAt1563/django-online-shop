from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from shop.recommender import Recommender

# you should import GTK3 for use weasyprint
# this for windows os
# you can download it from here
# https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
import os
os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\lib")
import weasyprint
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            # for make recommendation between the products
            # the bought togethers
            # so later the user can suggest these product to him
            # when buy one of them will suggest the others products
            r = Recommender()
            recommendation_for_products = []

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                recommendation_for_products.append(item['product'])

            r.products_bought(recommendation_for_products)

            cart.clear()

            # launch asynchronous task
            # for send message to the user email
            order_created.delay(order.id)

            # set the order in the session for use it by payment
            request.session['order_id'] = order.id
            # redirect for payment page
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})  # focus: create

# the user should be staff member to use this page
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # convert the html to sting and you can pass the variables
    # if it exist the html file
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    # apply the pdf name
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    # attach the pdf in the response

    # detect the html string and the source of the css files
    # then put it in the response after convert it to the pdf
    # by using weasyprint
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(
        settings.STATIC_ROOT+'\css\pdf.css')])
    return response
