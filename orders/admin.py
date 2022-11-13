from django.contrib import admin
from .models import Payment, Order, OrderedItem

class OrderedItemnline(admin.TabularInline):
    model = OrderedItem
    readonly_fields = ('order', 'payment', 'user', 'productitem', 'quantity', 'price', 'amount')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'is_ordered']
    inlines = [OrderedItemnline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem)

