from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, UserManager
from tc.utils import ROLES
from django.utils import timezone
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    role = models.CharField(choices=ROLES, max_length=50)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name if full_name else self.email

    @property
    def full_name(self):
        return self.get_full_name()


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
        return str(self.name)


class RepairItems(models.Model):
    Item_Id = models.CharField(max_length=50, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='items')
    Device = models.CharField(max_length=50, blank=True)
    Type = models.CharField(max_length=50)
    Model = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)

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
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='tickets')
    repairitems = models.CharField(max_length=100)

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
