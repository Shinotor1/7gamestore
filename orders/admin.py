from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Позиции заказа прямо на странице заказа — очень удобно."""
    model = OrderItem
    raw_id_fields = ['game']
    extra = 0 


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'user', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['email', 'user__username', 'id']
    inlines = [OrderItemInline]
  
    list_editable = ['status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'game', 'price']