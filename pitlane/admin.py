from django.contrib import admin
from .models import (
    Customer, Vehicle, Mechanic, Part, Service,
    Order, OrderStatus, OrderService, OrderPart,
    Invoice, Payment, Notification
)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "address", "date_joined")
    search_fields = ("first_name", "last_name", "email", "phone", "address")
    list_filter = ("date_joined",)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "vin", "owner")
    search_fields = ("brand", "model", "vin", "owner__name")
    list_filter = ("brand", "year")
    autocomplete_fields = ("owner",)

@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "hire_date", "is_active")
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = ("is_active", "hire_date")

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("name", "part_number", "price", "stock_quantity")
    search_fields = ("name", "part_number")
    list_filter = ("name",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    list_filter = ("name",)

class OrderServiceInline(admin.TabularInline):
    model = OrderService
    extra = 1
    autocomplete_fields = ("service",)

class OrderPartInline(admin.TabularInline):
    model = OrderPart
    extra = 1
    autocomplete_fields = ("part",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "vehicle", "mechanic", "order_date", "is_closed")
    search_fields = ("customer__name", "vehicle__vin", "mechanic__last_name")
    list_filter = ("is_closed", "order_date")
    autocomplete_fields = ("customer", "vehicle", "mechanic")
    inlines = [OrderServiceInline, OrderPartInline]

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "timestamp", "note")
    search_fields = ("order__id", "status")
    list_filter = ("status", "timestamp")

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "issue_date", "due_date", "total_amount", "is_paid")
    search_fields = ("order__id",)
    list_filter = ("is_paid", "issue_date", "due_date")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "payment_date", "amount", "payment_method")
    search_fields = ("invoice__id", "payment_method")
    list_filter = ("payment_method", "payment_date")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "timestamp")
    search_fields = ("message",)
    list_filter = ("timestamp",)

