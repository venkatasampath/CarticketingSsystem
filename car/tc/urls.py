from django.urls import path
from tc.views import *

app_name = 'tc'

urlpatterns = [
    path("", homepage, name='homepage'),
    path("staff-login/", staffLogin, name='staffLogin'),

    path("customer-login/", customerLogin, name='customerLogin'),
    path("staff-signup/", staffSignup, name='staffSignup'),

    path("customer-signup/", customerSignup, name='customerSignup'),
    path("logout/", user_logout, name='user_logout'),
]
