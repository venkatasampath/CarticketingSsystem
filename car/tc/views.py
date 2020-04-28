from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from django.template.loader import get_template

from tc.forms import *
from django.contrib.auth import authenticate, login, logout
from tc.models import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm



def staffSignup(request):
    if request.method == "GET":
        return render(request, "tc/staff_signup.html", {})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("email"),
                is_staff=True, role='staff'
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect(reverse("tc:homepage",))
        else:
            return render(
                request, "tc/staff_signup.html", {"errors": form.errors}
            )


def customerSignup(request):
    if request.method == "GET":
        return render(request, "tc/customer_signup.html", {})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("email"),
                is_customer=True, role='customer'
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect(reverse("tc:homepage",))
        else:
            return render(
                request, "tc/customer_signup.html", {"errors": form.errors}
            )


def customerLogin(request):
    if request.method == "GET":
        return render(request, "tc/customer_login.html", {})

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password,)
            if user is None:
                return render(
                    request,
                    "tc/customer_login.html",
                    {"errors": {"account_error": [
                        "Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active and user.is_customer:
                    login(request, user)
                    return HttpResponseRedirect(reverse("tc:homepage",))
                elif user.is_active and user.is_customer is False:
                    return render(
                        request,
                        "tc/customer_login.html",
                        {
                            "errors": {
                                "account_error": ["Email is not associated with Customer"]
                            }
                        },
                    )

                else:
                    return HttpResponse(
                        "# your account is inactive contact admin for details user@example.com"
                    )

            else:
                pass
        else:
            return render(request, "tc/customer_login.html", {"errors": form.errors})


def staffLogin(request):
    if request.method == "GET":
        return render(request, "tc/staff_login.html", {})

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password,)
            if user is None:
                return render(
                    request,
                    "tc/staff_login.html",
                    {"errors": {"account_error": [
                        "Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active and user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect(reverse("tc:homepage",))
                elif user.is_active and user.is_staff is False:
                    return render(
                        request,
                        "tc/staff_login.html",
                        {
                            "errors": {
                                "account_error": ["Email is not associated with Staff"]
                            }
                        },
                    )

                else:
                    return HttpResponse(
                        "# your account is inactive contact admin for details user@example.com"
                    )

            else:
                pass
        else:
            return render(request, "tc/staff_login.html", {"errors": form.errors})


def homepage(request):
    print('yessss')
    # return HttpResponse("test tc")
    return render(request, "tc/landing_page.html", {})


def user_logout(request):
    logout(request)
    return redirect(reverse("tc:homepage"))


def add_customer(request):
    if request.user.is_staff:
        form_name = 'Add Customer Details'
        if request.method == "GET":
            form = CustomerForm()
            return render(request, 'tc/form.html', {'form': form,"form_name":form_name})
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form = CustomerForm()
                return render(request, 'tc/form.html', {'form': form,"form_name":form_name})
        return redirect(reverse('tc:list_customer'))
    else:
        return HttpResponse("You are not authorized to access this page. Only staff users are authorized.")


def list_customer(request):
    if request.user.is_staff:
        customer_list = Customer.objects.all()
        return render(request, 'tc/customer_list.html', {'list_info': customer_list})
    else:
        return HttpResponse("You are not authorized to view this page. Only staff users are authorized.")


def edit_customer(request, user_id):
    if request.user.is_staff:
        form_name = 'Edit Customer Details'
        customer_data = get_object_or_404(Customer, pk=user_id)
        if request.method == "GET":
            form = CustomerForm(instance=customer_data)
            return render(request, 'tc/form.html', {'form': form,"form_name":form_name})
        if request.method == "POST":
            form = CustomerForm(request.POST, instance=customer_data)
            if form.is_valid():
                form.save()
            else:
                form = CustomerForm(instance=customer_data)
                return render(request, 'tc/form.html', {'form': form,"form_name":form_name})
        return redirect(reverse('tc:list_customer'))
    else:
        return HttpResponse("You are not authorized to access this page. Only staff users are authorized.")


def delete_customer(request, user_id):
    if request.user.is_staff:
        customer = get_object_or_404(Customer, pk=user_id)
        customer.delete()
        return redirect(reverse('tc:list_customer'))
    else:
        return HttpResponse("You are not authorized to access this page. Only staff users are authorized.")
def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'GET':
        return render(request, "tc/password_change_form.html", {"form": form})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(
                request, "tc/password_change_done.html", {}
            )
        return render(
            request, "tc/password_change_form.html", {"errors": form.errors}
        )


def view_Customer_tickets(request):
    if request.user.is_staff:
        customer_tickets = CustomerTickets.objects.all()
        return render(request, 'tc/customer_tickets_list.html', {'list_info': customer_tickets})
    elif request.user.is_customer:
        customer_tickets = CustomerTickets.objects.filter(
            customer__email=request.user.email)
        return render(request, 'tc/customer_tickets_list.html', {'list_info': customer_tickets})
    else:
        return HttpResponse("You are not authorized to access this page. Only staff users are authorized.")


def add_customer_ticket(request):
    if request.user.is_customer:
        form_name = 'Raise New Ticket'
        if request.method == "GET":
            form = CustomerTicketForm()
            return render(request, 'tc/form.html', {'form': form,"form_name":form_name})
        if request.method == "POST":
            form = CustomerTicketForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form = CustomerTicketForm(instance=request.POST)
                return render(request, 'tc/form.html', {'form': form,"form_name":form_name})
        return redirect(reverse('tc:homepage'))
    else:
        return HttpResponse("You are not authorized to access this page. Only customer users are authorized.")


def add_repair_items(request):
    if request.user.is_staff:
        form_name = 'Add Repair Items'
        if request.method == "GET":
            form = RepairItemsForm()
            return render(request, 'tc/form.html', {'form': form,"form_name":form_name})
        if request.method == "POST":
            form = RepairItemsForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form = RepairItemsForm(instance=request.POST)
                return render(request, 'tc/form.html', {'form': form,"form_name":form_name})
        return redirect(reverse('tc:homepage'))
    else:
        return HttpResponse("You are not authorized to access this page. Only staff users are authorized.")


class ResetPasswordRequestView(FormView):
    # code for template is given below the view's code
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy('tc:homepage')
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
        # uses the method written above
        if self.validate_email_address(data) is True:
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    print(user.pk, user, urlsafe_base64_encode(force_bytes(
                        user.pk)), default_token_generator.make_token(user))
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Car Tracking system',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'registration/password_reset_subject.txt'
                    # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                    email_template_name = 'registration/password_reset_email.html'
                    # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [
                              user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +
                                 ". Please check your inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(
                request, 'No user is associated with this email address')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy('tc:homepage')
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(
                    request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


from django.http import HttpResponse
from django.views.generic import View
from tc.utils import render_to_pdf
from django.template.loader import get_template


def customer_summary_pdf(request):
    customers = Customer.objects.all()
    context = {'customers': customers,}
    template = get_template('tc/customer_summary_pdf.html')
    html = template.render(context)
    pdf = render_to_pdf('tc/customer_summary_pdf.html', context)
    return pdf

