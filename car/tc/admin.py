from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, RepairItems, CustomerTickets


class CustomerList(admin.ModelAdmin):
    list_display = ('cust_number', 'name', 'city', 'cell_phone')
    list_filter = ('cust_number', 'name', 'city')
    search_fields = ('cust_number', 'name')
    ordering = ['cust_number']


class RepairItemsList(admin.ModelAdmin):
    list_display = ('Item_Id','customer', 'Type', 'Model',)
    list_filter = ('Item_Id','customer', 'Type')
    search_fields = ('Item_Id','customer', 'Type')
    ordering = ['Item_Id']


class CustomerTicketsList(admin.ModelAdmin):
    list_display = ('customer','repairitems','Issue', 'severity','Ticket_date')
    list_filter = ('customer','repairitems','Issue', 'severity')
    search_fields =('customer','repairitems','Issue', 'severity')
    ordering = ['customer']


admin.site.register(Customer, CustomerList)
admin.site.register(RepairItems, RepairItemsList)
admin.site.register(CustomerTickets, CustomerTicketsList)

