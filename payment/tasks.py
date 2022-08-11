from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

# for send the pdf of the order
# to the user when finished applied the payment form
@task
def payment_completed(order_id):
    """
     Task to send an e-mail notification when an order is
     successfully created.
     """
    order = Order.objects.get(id=order_id)

    subject = f'My Shop - order {order.id}'
    message = 'Please, find attached for your recent purchase'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

    html = render_to_string('orders/order/pdf.html', {'order': order})
    # we should send the message by bytes format cuz we use pdf
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT+'\css\pdf.css')]
    # put the pdf in the out:byte format
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # when send the message it will have an
    # attachment pdf file
    email.attach(f'order_{order_id}.pdf', out.getvalue(), 'application/pdf')
    email.send()