from typing import Optional, List
from pydantic import field_serializer
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja import Schema
from ninja.responses import Response
from django.contrib.auth.models import User
from datetime import datetime

from pitlane.models import *

api = NinjaAPI()

class UserOut(Schema):
    id:int
    first_name:str
    last_name:str
    username:str
    email:str

class UserCreate(Schema):
    username:str
    email:str
    password:str
    first_name:Optional[str] = ""
    last_name:Optional[str] = ""


### ENDPOINTS ###

@api.get("/user", response=List[UserOut])
def get_all_users(request):
    users = User.objects.all()
    return users

@api.get("/user/{user_id}", response=UserOut)
def get_single_user(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return Response(
            {"detail": f"User with id {user_id} not found"},
            status=404
        )

@api.post("/user", response={201: UserOut, 400:dict})
def create_user(request, payload:UserCreate):
    if User.objects.filter(username=payload.username).exists():
        return Response({"detail": "Username already exists"}, status=400)
    
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name = payload.last_name
    )

    return Response(UserOut.from_orm(user), status=201)


### Schemas (Data Transfer Objects) ###

# Customer
class CustomerOut(Schema):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    address: str
    date_joined: datetime

class CustomerCreate(Schema):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    address: str

class CustomerUpdate(Schema):  # Für PUT Requests
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

# Vehicle
class VehicleOut(Schema):
    id: int
    brand: str
    model: str
    year: int
    vin: str
    owner: CustomerOut

class VehicleCreate(Schema):
    brand: str
    model: str
    year: int
    vin: str
    owner_id: int

class VehicleUpdate(Schema):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    vin: Optional[str] = None
    owner_id: Optional[int] = None

# Mechanic
class MechanicOut(Schema):
    id: int
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    hire_date: Optional[str]
    is_active: bool

class MechanicCreate(Schema):
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    hire_date: Optional[str]
    is_active: bool

class MechanicUpdate(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    hire_date: Optional[str] = None
    is_active: Optional[bool] = None

# Part
class PartOut(Schema):
    id: int
    name: str
    part_number: str
    description: Optional[str]
    price: float
    stock_quantity: int

class PartCreate(Schema):
    name: str
    part_number: str
    description: Optional[str]
    price: float
    stock_quantity: int

class PartUpdate(Schema):
    name: Optional[str] = None
    part_number: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

# Service
class ServiceOut(Schema):
    id: int
    name: str
    description: Optional[str]
    price: float

class ServiceCreate(Schema):
    name: str
    description: Optional[str]
    price: float

class ServiceUpdate(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

# Order
class OrderOut(Schema):
    id: int
    customer_id: int
    vehicle_id: int
    mechanic_id: Optional[int]
    order_date: str
    description: Optional[str]
    is_closed: bool

class OrderCreate(Schema):
    customer_id: int
    vehicle_id: int
    mechanic_id: Optional[int]
    description: Optional[str]
    is_closed: bool

class OrderUpdate(Schema):
    customer_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    mechanic_id: Optional[int] = None
    description: Optional[str] = None
    is_closed: Optional[bool] = None

# OrderStatus
class OrderStatusOut(Schema):
    id: int
    order_id: int
    status: str
    timestamp: str
    note: Optional[str]

class OrderStatusCreate(Schema):
    order_id: int
    status: str
    note: Optional[str]

class OrderStatusUpdate(Schema):
    order_id: Optional[int] = None
    status: Optional[str] = None
    note: Optional[str] = None

# OrderService
class OrderServiceOut(Schema):
    id: int
    order_id: int
    service_id: int
    quantity: int

class OrderServiceCreate(Schema):
    order_id: int
    service_id: int
    quantity: int

class OrderServiceUpdate(Schema):
    quantity: Optional[int] = None

# OrderPart
class OrderPartOut(Schema):
    id: int
    order_id: int
    part_id: int
    quantity: int

class OrderPartCreate(Schema):
    order_id: int
    part_id: int
    quantity: int

class OrderPartUpdate(Schema):
    quantity: Optional[int] = None

# Invoice
class InvoiceOut(Schema):
    id: int
    order_id: int
    issue_date: str
    due_date: str
    total_amount: float
    is_paid: bool

class InvoiceCreate(Schema):
    order_id: int
    due_date: str
    total_amount: float
    is_paid: bool

class InvoiceUpdate(Schema):
    due_date: Optional[str] = None
    total_amount: Optional[float] = None
    is_paid: Optional[bool] = None

# Payment
class PaymentOut(Schema):
    id: int
    invoice_id: int
    payment_date: str
    amount: float
    payment_method: str
    note: Optional[str]

class PaymentCreate(Schema):
    invoice_id: int
    amount: float
    payment_method: str
    note: Optional[str]

class PaymentUpdate(Schema):
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    note: Optional[str] = None

# Notification
class NotificationOut(Schema):
    id: int
    message: str
    timestamp: str

class NotificationCreate(Schema):
    message: str

class NotificationUpdate(Schema):
    message: Optional[str] = None

### API Endpoints ###

# Helper function to convert queryset to list of schemas
def queryset_to_schemas(queryset, SchemaClass):
    return [SchemaClass.from_orm(item) for item in queryset]

### Customers ###
@api.get("/customers", response=List[CustomerOut])
def get_customers(request):
    """
    Ruft eine Liste aller Kunden ab.
    """
    customers = Customer.objects.all()
    return queryset_to_schemas(customers, CustomerOut)

@api.get("/customers/{customer_id}", response=CustomerOut)
def get_customer(request, customer_id: int):
    """
    Ruft einen bestimmten Kunden anhand seiner ID ab.
    """
    customer = get_object_or_404(Customer, id=customer_id)
    return CustomerOut.from_orm(customer)

@api.post("/customers", response={201: CustomerOut, 400: dict})
def create_customer(request, payload: CustomerCreate):
    """
    Erstellt einen neuen Kunden.
    """
    customer = Customer.objects.create(**payload.dict())
    return Response(CustomerOut.from_orm(customer), status=201)

@api.put("/customers/{customer_id}", response={200: CustomerOut, 404: dict})
def update_customer(request, customer_id: int, payload: CustomerUpdate):
    """
    Aktualisiert einen bestehenden Kunden.
    """
    customer = get_object_or_404(Customer, id=customer_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(customer, attr, value)
    customer.save()
    return CustomerOut.from_orm(customer)

@api.delete("/customers/{customer_id}", response={204: None, 404: dict})
def delete_customer(request, customer_id: int):
    """
    Löscht einen bestehenden Kunden.
    """
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return Response(None, status=204)

### Vehicles ###
@api.get("/vehicles", response=List[VehicleOut])
def get_vehicles(request):
    """
    Ruft eine Liste aller Fahrzeuge ab.
    """
    vehicles = Vehicle.objects.all()
    return queryset_to_schemas(vehicles, VehicleOut)

@api.get("/vehicles/{vehicle_id}", response=VehicleOut)
def get_vehicle(request, vehicle_id: int):
    """
    Ruft ein bestimmtes Fahrzeug anhand seiner ID ab.
    """
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return VehicleOut.from_orm(vehicle)

@api.post("/vehicles", response={201: VehicleOut, 400: dict})
def create_vehicle(request, payload: VehicleCreate):
    """
    Erstellt ein neues Fahrzeug.
    """
    owner = get_object_or_404(Customer, id=payload.owner_id)
    vehicle = Vehicle.objects.create(owner=owner, **payload.dict(exclude={"owner_id"}))
    return Response(VehicleOut.from_orm(vehicle), status=201)

@api.put("/vehicles/{vehicle_id}", response={200: VehicleOut, 404: dict})
def update_vehicle(request, vehicle_id: int, payload: VehicleUpdate):
    """
    Aktualisiert ein bestehendes Fahrzeug.
    """
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
     # Ensure the owner exists
    if payload.owner_id is not None:
        owner = get_object_or_404(Customer, id=payload.owner_id)
        vehicle.owner = owner

    for attr, value in payload.dict(exclude_unset=True, exclude={"owner_id"}).items():
        setattr(vehicle, attr, value)

    vehicle.save()
    return VehicleOut.from_orm(vehicle)

@api.delete("/vehicles/{vehicle_id}", response={204: None, 404: dict})
def delete_vehicle(request, vehicle_id: int):
    """
    Löscht ein bestehendes Fahrzeug.
    """
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    vehicle.delete()
    return Response(None, status=204)

### Mechanics ###
@api.get("/mechanics", response=List[MechanicOut])
def get_mechanics(request):
    """
    Ruft eine Liste aller Mechaniker ab.
    """
    mechanics = Mechanic.objects.all()
    return queryset_to_schemas(mechanics, MechanicOut)

@api.get("/mechanics/{mechanic_id}", response=MechanicOut)
def get_mechanic(request, mechanic_id: int):
    """
    Ruft einen bestimmten Mechaniker anhand seiner ID ab.
    """
    mechanic = get_object_or_404(Mechanic, id=mechanic_id)
    return MechanicOut.from_orm(mechanic)

@api.post("/mechanics", response={201: MechanicOut, 400: dict})
def create_mechanic(request, payload: MechanicCreate):
    """
    Erstellt einen neuen Mechaniker.
    """
    mechanic = Mechanic.objects.create(**payload.dict())
    return Response(MechanicOut.from_orm(mechanic), status=201)

@api.put("/mechanics/{mechanic_id}", response={200: MechanicOut, 404: dict})
def update_mechanic(request, mechanic_id: int, payload: MechanicUpdate):
    """
    Aktualisiert einen bestehenden Mechaniker.
    """
    mechanic = get_object_or_404(Mechanic, id=mechanic_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(mechanic, attr, value)
    mechanic.save()
    return MechanicOut.from_orm(mechanic)

@api.delete("/mechanics/{mechanic_id}", response={204: None, 404: dict})
def delete_mechanic(request, mechanic_id: int):
    """
    Löscht einen bestehenden Mechaniker.
    """
    mechanic = get_object_or_404(Mechanic, id=mechanic_id)
    mechanic.delete()
    return Response(None, status=204)

### Parts ###
@api.get("/parts", response=List[PartOut])
def get_parts(request):
    """
    Ruft eine Liste aller Teile ab.
    """
    parts = Part.objects.all()
    return queryset_to_schemas(parts, PartOut)

@api.get("/parts/{part_id}", response=PartOut)
def get_part(request, part_id: int):
    """
    Ruft ein bestimmtes Teil anhand seiner ID ab.
    """
    part = get_object_or_404(Part, id=part_id)
    return PartOut.from_orm(part)

@api.post("/parts", response={201: PartOut, 400: dict})
def create_part(request, payload: PartCreate):
    """
    Erstellt ein neues Teil.
    """
    part = Part.objects.create(**payload.dict())
    return Response(PartOut.from_orm(part), status=201)

@api.put("/parts/{part_id}", response={200: PartOut, 404: dict})
def update_part(request, part_id: int, payload: PartUpdate):
    """
    Aktualisiert ein bestehendes Teil.
    """
    part = get_object_or_404(Part, id=part_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(part, attr, value)
    part.save()
    return PartOut.from_orm(part)

@api.delete("/parts/{part_id}", response={204: None, 404: dict})
def delete_part(request, part_id: int):
    """
    Löscht ein bestehendes Teil.
    """
    part = get_object_or_404(Part, id=part_id)
    part.delete()
    return Response(None, status=204)

### Services ###
@api.get("/services", response=List[ServiceOut])
def get_services(request):
    """
    Ruft eine Liste aller Dienstleistungen ab.
    """
    services = Service.objects.all()
    return queryset_to_schemas(services, ServiceOut)

@api.get("/services/{service_id}", response=ServiceOut)
def get_service(request, service_id: int):
    """
    Ruft eine bestimmte Dienstleistung anhand ihrer ID ab.
    """
    service = get_object_or_404(Service, id=service_id)
    return ServiceOut.from_orm(service)

@api.post("/services", response={201: ServiceOut, 400: dict})
def create_service(request, payload: ServiceCreate):
    """
    Erstellt eine neue Dienstleistung.
    """
    service = Service.objects.create(**payload.dict())
    return Response(ServiceOut.from_orm(service), status=201)

@api.put("/services/{service_id}", response={200: ServiceOut, 404: dict})
def update_service(request, service_id: int, payload: ServiceUpdate):
    """
    Aktualisiert eine bestehende Dienstleistung.
    """
    service = get_object_or_404(Service, id=service_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(service, attr, value)
    service.save()
    return ServiceOut.from_orm(service)

@api.delete("/services/{service_id}", response={204: None, 404: dict})
def delete_service(request, service_id: int):
    """
    Löscht eine bestehende Dienstleistung.
    """
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return Response(None, status=204)

### Orders ###
@api.get("/orders", response=List[OrderOut])
def get_orders(request):
    """
    Ruft eine Liste aller Aufträge ab.
    """
    orders = Order.objects.all()
    return queryset_to_schemas(orders, OrderOut)

@api.get("/orders/{order_id}", response=OrderOut)
def get_order(request, order_id: int):
    """
    Ruft einen bestimmten Auftrag anhand seiner ID ab.
    """
    order = get_object_or_404(Order, id=order_id)
    return OrderOut.from_orm(order)

@api.post("/orders", response={201: OrderOut, 400: dict})
def create_order(request, payload: OrderCreate):
    """
    Erstellt einen neuen Auftrag.
    """
    customer = get_object_or_404(Customer, id=payload.customer_id)
    vehicle = get_object_or_404(Vehicle, id=payload.vehicle_id)
    mechanic = get_object_or_404(Mechanic, id=payload.mechanic_id) if payload.mechanic_id else None
    order = Order.objects.create(customer=customer, vehicle=vehicle, mechanic=mechanic, **payload.dict(exclude={"customer_id", "vehicle_id", "mechanic_id"}))
    return Response(OrderOut.from_orm(order), status=201)

@api.put("/orders/{order_id}", response={200: OrderOut, 404: dict})
def update_order(request, order_id: int, payload: OrderUpdate):
    """
    Aktualisiert einen bestehenden Auftrag.
    """
    order = get_object_or_404(Order, id=order_id)

    # Handle foreign key updates
    if payload.customer_id is not None:
        customer = get_object_or_404(Customer, id=payload.customer_id)
        order.customer = customer
    if payload.vehicle_id is not None:
        vehicle = get_object_or_404(Vehicle, id=payload.vehicle_id)
        order.vehicle = vehicle
    if payload.mechanic_id is not None:
        mechanic = get_object_or_404(Mechanic, id=payload.mechanic_id)
        order.mechanic = mechanic

    # Update other attributes
    for attr, value in payload.dict(exclude_unset=True, exclude={"customer_id", "vehicle_id", "mechanic_id"}).items():
        setattr(order, attr, value)

    order.save()
    return OrderOut.from_orm(order)

@api.delete("/orders/{order_id}", response={204: None, 404: dict})
def delete_order(request, order_id: int):
    """
    Löscht einen bestehenden Auftrag.
    """
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return Response(None, status=204)

### OrderStatuses ###
@api.get("/orderstatuses", response=List[OrderStatusOut])
def get_orderstatuses(request):
    """
    Ruft eine Liste aller Auftragsstatus ab.
    """
    orderstatuses = OrderStatus.objects.all()
    return queryset_to_schemas(orderstatuses, OrderStatusOut)

@api.get("/orderstatuses/{orderstatus_id}", response=OrderStatusOut)
def get_orderstatus(request, orderstatus_id: int):
    """
    Ruft einen bestimmten Auftragsstatus anhand seiner ID ab.
    """
    orderstatus = get_object_or_404(OrderStatus, id=orderstatus_id)
    return OrderStatusOut.from_orm(orderstatus)

@api.post("/orderstatuses", response={201: OrderStatusOut, 400: dict})
def create_orderstatus(request, payload: OrderStatusCreate):
    """
    Erstellt einen neuen Auftragsstatus.
    """
    order = get_object_or_404(Order, id=payload.order_id)
    orderstatus = OrderStatus.objects.create(order=order, **payload.dict(exclude={"order_id"}))
    return Response(OrderStatusOut.from_orm(orderstatus), status=201)

@api.put("/orderstatuses/{orderstatus_id}", response={200: OrderStatusOut, 404: dict})
def update_orderstatus(request, orderstatus_id: int, payload: OrderStatusUpdate):
    """
    Aktualisiert einen bestehenden Auftragsstatus.
    """
    orderstatus = get_object_or_404(OrderStatus, id=orderstatus_id)
     # Ensure the order exists
    if payload.order_id is not None:
        order = get_object_or_404(Order, id=payload.order_id)
        orderstatus.order = order

    for attr, value in payload.dict(exclude_unset=True, exclude={"order_id"}).items():
        setattr(orderstatus, attr, value)

    orderstatus.save()
    return OrderStatusOut.from_orm(orderstatus)

@api.delete("/orderstatuses/{orderstatus_id}", response={204: None, 404: dict})
def delete_orderstatus(request, orderstatus_id: int):
    """
    Löscht einen bestehenden Auftragsstatus.
    """
    orderstatus = get_object_or_404(OrderStatus, id=orderstatus_id)
    orderstatus.delete()
    return Response(None, status=204)

### OrderServices ###
@api.get("/orderservices", response=List[OrderServiceOut])
def get_orderservices(request):
    """
    Ruft eine Liste aller Auftragsdienstleistungen ab.
    """
    orderservices = OrderService.objects.all()
    return queryset_to_schemas(orderservices, OrderServiceOut)

@api.get("/orderservices/{orderservice_id}", response=OrderServiceOut)
def get_orderservice(request, orderservice_id: int):
    """
    Ruft eine bestimmte Auftragsdienstleistung anhand ihrer ID ab.
    """
    orderservice = get_object_or_404(OrderService, id=orderservice_id)
    return OrderServiceOut.from_orm(orderservice)

@api.post("/orderservices", response={201: OrderServiceOut, 400: dict})
def create_orderservice(request, payload: OrderServiceCreate):
    """
    Erstellt eine neue Auftragsdienstleistung.
    """
    order = get_object_or_404(Order, id=payload.order_id)
    service = get_object_or_404(Service, id=payload.service_id)
    orderservice = OrderService.objects.create(order=order, service=service, **payload.dict(exclude={"order_id", "service_id"}))
    return Response(OrderServiceOut.from_orm(orderservice), status=201)

@api.put("/orderservices/{orderservice_id}", response={200: OrderServiceOut, 404: dict})
def update_orderservice(request, orderservice_id: int, payload: OrderServiceUpdate):
    """
    Aktualisiert eine bestehende Auftragsdienstleistung.
    """
    orderservice = get_object_or_404(OrderService, id=orderservice_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(orderservice, attr, value)

    orderservice.save()
    return OrderServiceOut.from_orm(orderservice)

@api.delete("/orderservices/{orderservice_id}", response={204: None, 404: dict})
def delete_orderservice(request, orderservice_id: int):
    """
    Löscht eine bestehende Auftragsdienstleistung.
    """
    orderservice = get_object_or_404(OrderService, id=orderservice_id)
    orderservice.delete()
    return Response(None, status=204)

### OrderParts ###
@api.get("/orderparts", response=List[OrderPartOut])
def get_orderparts(request):
    """
    Ruft eine Liste aller Auftragsbestandteile ab.
    """
    orderparts = OrderPart.objects.all()
    return queryset_to_schemas(orderparts, OrderPartOut)

@api.get("/orderparts/{orderpart_id}", response=OrderPartOut)
def get_orderpart(request, orderpart_id: int):
    """
    Ruft einen bestimmten Auftragsbestandteil anhand seiner ID ab.
    """
    orderpart = get_object_or_404(OrderPart, id=orderpart_id)
    return OrderPartOut.from_orm(orderpart)

@api.post("/orderparts", response={201: OrderPartOut, 400: dict})
def create_orderpart(request, payload: OrderPartCreate):
    """
    Erstellt einen neuen Auftragsbestandteil.
    """
    order = get_object_or_404(Order, id=payload.order_id)
    part = get_object_or_404(Part, id=payload.part_id)
    orderpart = OrderPart.objects.create(order=order, part=part, **payload.dict(exclude={"order_id", "part_id"}))
    return Response(OrderPartOut.from_orm(orderpart), status=201)

@api.put("/orderparts/{orderpart_id}", response={200: OrderPartOut, 404: dict})
def update_orderpart(request, orderpart_id: int, payload: OrderPartUpdate):
    """
    Aktualisiert einen bestehenden Auftragsbestandteil.
    """
    orderpart = get_object_or_404(OrderPart, id=orderpart_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(orderpart, attr, value)

    orderpart.save()
    return OrderPartOut.from_orm(orderpart)

@api.delete("/orderparts/{orderpart_id}", response={204: None, 404: dict})
def delete_orderpart(request, orderpart_id: int):
    """
    Löscht einen bestehenden Auftragsbestandteil.
    """
    orderpart = get_object_or_404(OrderPart, id=orderpart_id)
    orderpart.delete()
    return Response(None, status=204)

### Invoices ###
@api.get("/invoices", response=List[InvoiceOut])
def get_invoices(request):
    """
    Ruft eine Liste aller Rechnungen ab.
    """
    invoices = Invoice.objects.all()
    return queryset_to_schemas(invoices, InvoiceOut)

@api.get("/invoices/{invoice_id}", response=InvoiceOut)
def get_invoice(request, invoice_id: int):
    """
    Ruft eine bestimmte Rechnung anhand ihrer ID ab.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return InvoiceOut.from_orm(invoice)

@api.post("/invoices", response={201: InvoiceOut, 400: dict})
def create_invoice(request, payload: InvoiceCreate):
    """
    Erstellt eine neue Rechnung.
    """
    order = get_object_or_404(Order, id=payload.order_id)
    invoice = Invoice.objects.create(order=order, **payload.dict(exclude={"order_id"}))
    return Response(InvoiceOut.from_orm(invoice), status=201)

@api.put("/invoices/{invoice_id}", response={200: InvoiceOut, 404: dict})
def update_invoice(request, invoice_id: int, payload: InvoiceUpdate):
    """
    Aktualisiert eine bestehende Rechnung.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(invoice, attr, value)

    invoice.save()
    return InvoiceOut.from_orm(invoice)

@api.delete("/invoices/{invoice_id}", response={204: None, 404: dict})
def delete_invoice(request, invoice_id: int):
    """
    Löscht eine bestehende Rechnung.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return Response(None, status=204)

### Payments ###
@api.get("/payments", response=List[PaymentOut])
def get_payments(request):
    """
    Ruft eine Liste aller Zahlungen ab.
    """
    payments = Payment.objects.all()
    return queryset_to_schemas(payments, PaymentOut)

@api.get("/payments/{payment_id}", response=PaymentOut)
def get_payment(request, payment_id: int):
    """
    Ruft eine bestimmte Zahlung anhand ihrer ID ab.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    return PaymentOut.from_orm(payment)

@api.post("/payments", response={201: PaymentOut, 400: dict})
def create_payment(request, payload: PaymentCreate):
    """
    Erstellt eine neue Zahlung.
    """
    invoice = get_object_or_404(Invoice, id=payload.invoice_id)
    payment = Payment.objects.create(invoice=invoice, **payload.dict(exclude={"invoice_id"}))
    return Response(PaymentOut.from_orm(payment), status=201)

@api.put("/payments/{payment_id}", response={200: PaymentOut, 404: dict})
def update_payment(request, payment_id: int, payload: PaymentUpdate):
    """
    Aktualisiert eine bestehende Zahlung.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(payment, attr, value)

    payment.save()
    return PaymentOut.from_orm(payment)

@api.delete("/payments/{payment_id}", response={204: None, 404: dict})
def delete_payment(request, payment_id: int):
    """
    Löscht eine bestehende Zahlung.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    return Response(None, status=204)

### Notifications ###
@api.get("/notifications", response=List[NotificationOut])
def get_notifications(request):
    """
    Ruft eine Liste aller Benachrichtigungen ab.
    """
    notifications = Notification.objects.all()
    return queryset_to_schemas(notifications, NotificationOut)

@api.get("/notifications/{notification_id}", response=NotificationOut)
def get_notification(request, notification_id: int):
    """
    Ruft eine bestimmte Benachrichtigung anhand ihrer ID ab.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    return NotificationOut.from_orm(notification)

@api.post("/notifications", response={201: NotificationOut, 400: dict})
def create_notification(request, payload: NotificationCreate):
    """
    Erstellt eine neue Benachrichtigung.
    """
    notification = Notification.objects.create(**payload.dict())
    return Response(NotificationOut.from_orm(notification), status=201)

@api.put("/notifications/{notification_id}", response={200: NotificationOut, 404: dict})
def update_notification(request, notification_id: int, payload: NotificationUpdate):
    """
    Aktualisiert eine bestehende Benachrichtigung.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(notification, attr, value)

    notification.save()
    return NotificationOut.from_orm(notification)

@api.delete("/notifications/{notification_id}", response={204: None, 404: dict})
def delete_notification(request, notification_id: int):
    """
    Löscht eine bestehende Benachrichtigung.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    return Response(None, status=204)

### Spezielle Endpoints ###

@api.get("/orders/{order_id}/statuses", response=List[OrderStatusOut])
def get_order_statuses(request, order_id: int):
    """
    Ruft alle Status-Änderungen für einen bestimmten Auftrag ab.
    """
    order = get_object_or_404(Order, id=order_id)
    statuses = OrderStatus.objects.filter(order=order)
    return queryset_to_schemas(statuses, OrderStatusOut)

@api.get("/vehicles/customer/{customer_id}", response=List[VehicleOut])
def get_vehicles_for_customer(request, customer_id: int):
    """
    Ruft alle Fahrzeuge eines bestimmten Kunden ab.
    """
    customer = get_object_or_404(Customer, id=customer_id)
    vehicles = Vehicle.objects.filter(owner=customer)
    return queryset_to_schemas(vehicles, VehicleOut)

@api.get("/invoices/order/{order_id}", response=Optional[InvoiceOut])
def get_invoice_for_order(request, order_id: int):
    """
    Ruft die Rechnung für einen bestimmten Auftrag ab (falls vorhanden).
    """
    order = get_object_or_404(Order, id=order_id)
    try:
        invoice = Invoice.objects.get(order=order)
        return InvoiceOut.from_orm(invoice)
    except Invoice.DoesNotExist:
        return None  # Oder eine Fehlerantwort, je nach Bedarf

@api.get("/parts/search", response=List[PartOut])
def search_parts(request, query: str):
    """
    Sucht Teile anhand des Namens oder der Teilenummer.
    """
    parts = Part.objects.filter(
        Q(name__icontains=query) | Q(part_number__icontains=query)
    )
    return queryset_to_schemas(parts, PartOut)

@api.post("/orders/{order_id}/add_service/{service_id}", response={201: OrderServiceOut, 404: dict})
def add_service_to_order(request, order_id: int, service_id: int, quantity: int = 1):
    """
    Fügt eine Dienstleistung zu einem Auftrag hinzu.
    """
    order = get_object_or_404(Order, id=order_id)
    service = get_object_or_404(Service, id=service_id)
    order_service = OrderService.objects.create(order=order, service=service, quantity=quantity)
    return Response(OrderServiceOut.from_orm(order_service), status=201)

@api.post("/orders/{order_id}/add_part/{part_id}", response={201: OrderPartOut, 404: dict})
def add_part_to_order(request, order_id: int, part_id: int, quantity: int = 1):
    """
    Fügt ein Teil zu einem Auftrag hinzu.
    """
    order = get_object_or_404(Order, id=order_id)
    part = get_object_or_404(Part, id=part_id)
    order_part = OrderPart.objects.create(order=order, part=part, quantity=quantity)
    return Response(OrderPartOut.from_orm(order_part), status=201)

@api.put("/invoices/{invoice_id}/mark_paid", response={200: InvoiceOut, 404: dict})
def mark_invoice_as_paid(request, invoice_id: int):
    """
    Markiert eine Rechnung als bezahlt.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.is_paid = True
    invoice.save()
    return InvoiceOut.from_orm(invoice)

@api.get("/mechanics/available", response=List[MechanicOut])
def get_available_mechanics(request):
    """
    Ruft alle aktiven Mechaniker ab, die derzeit keinem Auftrag zugewiesen sind.  (Annahme: mechanic Feld in Order kann Null sein, wenn kein Mechaniker zugewiesen ist)
    """
    # Finde Mechaniker, die nicht in einem noch offenen Auftrag sind
    assigned_mechanic_ids = Order.objects.filter(is_closed=False, mechanic__isnull=False).values_list('mechanic_id', flat=True).distinct()
    available_mechanics = Mechanic.objects.filter(is_active=True).exclude(id__in=assigned_mechanic_ids)
    return queryset_to_schemas(available_mechanics, MechanicOut)

