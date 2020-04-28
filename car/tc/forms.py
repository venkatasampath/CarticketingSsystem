from django import forms
from tc.models import User
from tc.models import *


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)


class SignUpForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            if user.is_staff:
                user_role = "Staff"

            else:
                user_role = "Customer"
            raise forms.ValidationError(
                "{} with this email already exists, use another email.".format(
                    user_role
                )
            )
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise forms.ValidationError(
                "Password should be minimum 6 characters long")

        if password != self.data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return password


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ('created_date', 'updated_date')


class CustomerTicketForm(forms.ModelForm):
    class Meta:
        model = CustomerTickets
        # exclude = ('customer',)
        exclude = ()


class RepairItemsForm(forms.ModelForm):
    class Meta:
        model = RepairItems
        exclude = ()


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label=("Email"), max_length=254)


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2