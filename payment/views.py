import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from .tasks import payment_completed

# instantiate Braintree payment gateway
# for make gateway between the page and the bank
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # retrieve nonce form content
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transcation
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                #  the transaction is automatically submitted for settlement
                'submit_for_settlement': True,
            }
        })

        # if the form fields is correct and there is enough money
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()

            # launch asynchronous task
            # send pdf detail for the order to the user email
            payment_completed.delay(order.id)
            return redirect('payment:done')
        return redirect('payment:canceled')

    else:
        # generate token for use it in the template form
        # for make access on the gateway
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {
            'order': order,
            'client_token': client_token,
        })

# when applied right values
def payment_done(request):
    return render(request, 'payment/done.html')

# when applied wrong values
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
