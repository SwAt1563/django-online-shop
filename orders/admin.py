from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe



# if you want to make function
# applied on selected orders in the administration page
# for the list of orders
# you should make function with these parameters
# (modeladmin, request, queryset)
def export_to_csv(modeladmin, request, queryset):
    # for get the options of the current model
    opts = modeladmin.model._meta
    # opts.verbose_name: get the model name
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    # apply the file name
    response['Content-Disposition'] = content_disposition
    # make writer function for write in the csv file
    # build by the response
    writer = csv.writer(response)

    # get all fields names except the fields which have relations
    fields = [field for field in opts.get_fields() if not
    field.many_to_many and not field.one_to_many]

    # write the first row for column names
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            # for apply different format on the date then save it
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


# short name applied on the column
export_to_csv.short_description = 'Export to csv'


# functions applied in the administration page
# in order list page for each order
# you can see the detail for it
def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    # for return save html mark we used this function
    # instead of return normal string in django
    return mark_safe(f'<a href="{url}">View</a>')

# functions applied in the administration page
# in order list page for each order
# you can see the pdf for it
def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


# for let create the order item in the
# order creation page in the administration page
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # for apply the two pages of order_detail and order_pdf
    # in the list display page of order
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']

    inlines = (OrderItemInline,)
    actions = (export_to_csv,)  # apply the action in the order list page
