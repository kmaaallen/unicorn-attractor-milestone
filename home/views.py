from django.shortcuts import render, redirect
from home.forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.


def landing_page(request):
    """
    A view that displays the landing page
    """
    return render(request, 'index.html')


def find_out_more(request):
    """
    A view that displays the find out more page
    """
    return render(request, 'more.html')


def contact_us(request):
    """
    A view that displays the contact us page and sends email
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            sender_name = contact_form.cleaned_data['name']
            sender_email = contact_form.cleaned_data['email']
            message = ('{0} has sent you a new message:\n\n{1} \n\nTheir'
                       ' contact'
                       ' email '
                       'is: {2}').format(sender_name,
                                         contact_form.cleaned_data['message'],
                                         sender_email)
            send_mail('Contact Form', message, sender_email,
                      [settings.EMAIL_HOST_USER])
            request.session['contacted'] = True
            return redirect('thanks')
    else:
        if request.user:
            contact_form = ContactForm(initial={
                                      'name': request.user.first_name,
                                      'email': request.user.email})
        else:
            contact_form = ContactForm()
    return render(request, 'contact.html', {"contact_form": contact_form})


def thanks(request):
    """
    A view that displays the thank you message after using contact form
    """
    if 'contacted' in request.session:
        return render(request, 'thanks.html')
    else:
        return redirect('contact_us')
