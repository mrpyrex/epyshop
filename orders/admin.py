import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields(
    ) if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export To CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0
    template = 'admin/order/tabular.html'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'quantity', 'order']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'phone',
                    'billing_address1', 'amount', 'billing_address2', 'city', 'created_at', 'updated_at', 'paid']
    list_filter = ['created_at', 'updated_at', 'paid']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    readonly_fields = ['id', 'amount', 'ref', 'phone',
                       'billing_address1', 'billing_address2', 'city', 'created_at', 'updated_at', 'paid']
    fieldsets = [
        ('ORDER INFORMATION', {'fields': [
         'id', 'ref', 'created_at', 'amount']}),
        ('SHIPPING INFORMATION', {'fields': ['phone',
                                             'billing_address1', 'billing_address2', 'city']})
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
