from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from accounts.forms import UserSignInForm, UserSignUpForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

# Create your views here.


@login_required
def sign_out(request):
    """Logs out user"""
    auth.logout(request)
    return redirect(reverse('index'))


def sign_in(request):
    """ Return sign up template """
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        sign_in_form = UserSignInForm(request.POST)
        if sign_in_form.is_valid():
            user = auth.authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully signed in!")
                return redirect(reverse('index'))
            else:
                sign_in_form.add_error(
                    None,
                    "Your username and password combination is incorrect")
    else:
        sign_in_form = UserSignInForm()
    return render(request, 'sign_in.html', {"sign_in_form": sign_in_form})


def sign_up(request):
    """ render the sign up page """
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        sign_up_form = UserSignUpForm(request.POST)

        if sign_up_form.is_valid():
            sign_up_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully signed up")
            else:
                messages.error(
                    request, "Unable to sign you up at this time")
    else:
        sign_up_form = UserSignUpForm()
    return render(request, 'sign_up.html', {"sign_up_form": sign_up_form})

# def user_profile(request):
#     """ the user's profile page """
#     user = User.objects.get(email=request.user.email)
#     return render(request, 'profile.html', {"profile": user})
