from django.urls import path
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse, get_object_or_404

from tc.views import *
from . import views

app_name = 'tc'

urlpatterns = [
    path("change-password/", views.change_password, name="change_password"),
    path("", homepage, name='homepage'),
    path("staff-login/", staffLogin, name='staffLogin'),

    path("customer-login/", customerLogin, name='customerLogin'),
    path("staff-signup/", staffSignup, name='staffSignup'),

    path("customer-signup/", customerSignup, name='customerSignup'),
    path("logout/", user_logout, name='user_logout'),

    # customer crud operations
    path('add/new/customers/', add_customer, name='add_customer'),
    path('list/customers/info/', list_customer, name='list_customer'),
    path('edit/customer/<int:user_id>/', edit_customer, name='edit_customer'),
    path('delete/customer/<int:user_id>/',
         delete_customer, name='delete_customer'),

    # customer tickets
    path('list/customers-tickets/info/',
         view_Customer_tickets, name='view_Customer_tickets'),
    path('add/new/customer-ticket/', add_customer_ticket,
         name='add_customer_ticket'),
    path('customer_pdf/', views.customer_summary_pdf,name='customer_summary_pdf'),

    # add repairitems
    path('add/repair-items/', add_repair_items, name='add_repair_items'),

    # password-reset
    path('account/reset_password', ResetPasswordRequestView.as_view(), name="reset_password"),
    path('account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='reset_password_confirm'),

]

