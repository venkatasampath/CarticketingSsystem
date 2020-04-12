from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from tc.forms import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.


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
                    {"errors": {"account_error": ["Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active and user.is_customer:
                    login(request, user)
                    return HttpResponseRedirect(reverse("tc:homepage",))
                elif user.is_active and user.is_volunteer is False:
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
                    {"errors": {"account_error": ["Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active and user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect(reverse("tc:homepage",))
                elif user.is_active and user.is_volunteer is False:
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

