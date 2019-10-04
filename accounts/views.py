from django.shortcuts import render
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import ShopUser

from django.contrib.auth import get_user_model
User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.phone = form.cleaned_data['phone']
            user.city = form.cleaned_data['city']
            user.save()

            current_site = get_current_site(request)
            mail_subject = "activate your account."
            message = render_to_string('active_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.add_message(request, messages.SUCCESS,'Please confirm your Emaill address to complete the registration', extra_tags='someclass')
            # return HttpResponse('Please confirm your email address to complete the registration')
            return render(request, 'pages/index.html')

    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token) and not user.is_active:
        user.is_active = True
        user.save()
        login(request, user)
        # return HttpResponse('Thanks for activation and signup ... ')
        messages.add_message(request, messages.SUCCESS, 'Thanks for activation ...',
                             extra_tags='someclass')
        return render(request, 'pages/index.html')
    else:
        return HttpResponse('Activation link is invalid!')