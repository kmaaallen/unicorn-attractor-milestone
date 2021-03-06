from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from accounts.forms import UserSignInForm, UserSignUpForm
from django.contrib.auth.decorators import login_required


@login_required
def sign_out(request):
    """Logs out user

    Arguments:
    request = HttpRequest object
    """
    auth.logout(request)
    return redirect(reverse('sign_in'))


def sign_in(request):
    """ Return sign in template

    Arguments:
    request = HttpRequest object
    """
    if request.user.is_authenticated:
        return redirect('landing_page')
    if request.method == "POST":
        sign_in_form = UserSignInForm(request.POST)
        if sign_in_form.is_valid():
            user = auth.authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                return redirect('find_out_more')
            else:
                sign_in_form.add_error(
                    None,
                    "Your username and password combination is incorrect")
    else:
        sign_in_form = UserSignInForm()
    return render(request, 'sign_in.html', {"sign_in_form": sign_in_form})


def sign_up(request):
    """ render the sign up page

    Arguments:
    request = HttpRequest object
    """
    if request.user.is_authenticated:
        return redirect('landing_page')

    if request.method == "POST":
        sign_up_form = UserSignUpForm(request.POST)

        if sign_up_form.is_valid():
            sign_up_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully signed up",
                                 extra_tags='alert-success')
                return render(request, 'more.html')
            else:
                messages.error(
                    request, "Unable to sign you up at this time",
                    extra_tags='alert-error')
    else:
        sign_up_form = UserSignUpForm()
    return render(request, 'sign_up.html', {"sign_up_form": sign_up_form})


@login_required
def user_profile(request):
    """Show user's profile page

    Arguments:
    request = HttpRequest object
    """
    user = request.user
    return render(request, 'user_profile.html', {"user": user})
