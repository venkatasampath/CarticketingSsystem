from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import requests


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cust_number = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_number)


class RepairItems(models.Model):
    Item_Id = models.CharField(max_length=50, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='items')
    Device = models.CharField(max_length=50, blank=True)
    Type = models.CharField(max_length=50)
    Model = models.CharField(max_length=50)
    description = models.CharField(max_length=200,blank=True)
 #   Due_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.Item_Id)


class CustomerTickets(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets')
    repairitems = models.ForeignKey(RepairItems, on_delete=models.CASCADE, related_name='repairitems', default='Item_Id', blank=True)
#    Model = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='tickets')
    Issue = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
#    Issue_date = models.DateField(default=timezone.now)
    Ticket_date = models.DateField(default=timezone.now)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.repairitems)







