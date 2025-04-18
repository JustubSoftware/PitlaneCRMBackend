from django.db import models

# Create your models here.

class Customer(models.Model):
    """
    this model saves information about the customer
    """

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Vehicle(models.Model):
    """
    stores vehicle details and links them to a customer
    """

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=150)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True) # Vehicle identification Number
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
class Mechanic(models.Model):
    """Stores mechanic/employee details."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Service(models.Model):
    """
    stores details about the services offered by the workshop
    """

class Part(models.Model):
    """Stores information about parts in stock."""
    name = models.CharField(max_length=100)
    part_number = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.part_number})"

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    """Stores details about services offered by the workshop."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    """Represents a repair order for a customer's vehicle."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.customer.name} - {self.vehicle.make} {self.vehicle.model}"

class OrderStatus(models.Model):
    """Tracks the status of an order over time."""
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('in_progress', 'In Progress'),
        ('waiting_for_parts', 'Waiting for Parts'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='received')
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Status: {self.status} - Order {self.order.id}"

class OrderService(models.Model):
    """Links orders with the services provided and tracks the quantity."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.service.name} - Order {self.order.id}"
    
class OrderPart(models.Model):
    """Tracks which parts were used for an order and in what quantity."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='parts')
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.part.name} - Order {self.order.id}"
    
class Invoice(models.Model):
    """Represents an invoice generated for an order."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.id} - Order {self.order.id}"
    
class Payment(models.Model):
    """Tracks payments made for invoices."""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ])
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Payment {self.amount} for Invoice {self.invoice.id}"
    
class Notification(models.Model):
    """Stores notifications sent to users."""
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message