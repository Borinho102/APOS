from django.contrib.auth.models import User
from django.contrib.auth.views import *
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView
from django_registration import signals
from django_registration.backends.activation.views import RegistrationView
from django.core.mail import EmailMessage
from Account.models import UserData
from phonenumber_field.modelfields import PhoneNumber
from Account.forms import ResetForm, RegForm


# Create your views here.

class PasswordResetViewer(PasswordResetView):
    template_name = 'registration/reset.html'
    html_email_template_name = 'mail/Reset_email.html'
    form_class = ResetForm
    success_url = '/accounts/reset/done/'
    subject_template_name = 'mail/Reset.txt'


class PasswordResetDoneViewer(PasswordResetDoneView):
    template_name = 'registration/reset_done.html'
    title = 'Reset Done | MIM'


class PasswordResetConfirmViewer(PasswordResetConfirmView):
    title = 'Reset Account | MIM'
    success_url = '/reset/done/'
    template_name = 'registration/reset_confirm.html'


class PasswordResetCompleteViewer(PasswordResetCompleteView):
    template_name = 'registration/reset_finish.html'


class RegistrationViewer(RegistrationView):
    template_name = "registration/registration.html"
    success_url = "/registration/done/"
    form_class = RegForm
    email_subject_template = 'mail/activation_email_subject.txt'
    email_body_template = 'mail/activation_email_body.html'
    disallowed_url = '/accounts/register/fail'

    def register(self, form):
        print(self.request.POST['phone_1'])
        print(self.request.POST['phone_0'])
        new_user = self.create_inactive_user(form)
        signals.user_registered.send(
            sender=self.__class__,
            user=new_user,
            request=self.request
        )
        return new_user

    def create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions.
        """
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.email = self.request.POST['email']
        new_user.last_name = self.request.POST['last_name'].capitalize()
        new_user.first_name = self.request.POST['first_name'].upper()
        new_user.username = self.request.POST['username']
        if new_user:
            new_user.save()
            u = UserData.objects.create(
                user=new_user,
                phone=PhoneNumber(country_code=self.request.POST['phone_0'], national_number=self.request.POST['phone_1']),
                avatar=self.request.POST.get('profile')
            )
            u.save()
            self.send_activation_email(new_user)
        return new_user

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context['user'] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            template_name=self.email_body_template,
            context=context,
            request=self.request
        )
        m = EmailMessage(
            subject=subject, body=message, from_email="mail@apos.org",
            to=[user.email]
        )
        m.content_subtype = 'html'
        m.send()


class Panel(TemplateView):
    http_method_names = ['get', ]

    def get(self, request, **kwargs):
        pass


def reg_fail(request):
    return render(request, "registration/register_fail.html", None)


def reg_done(request):
    return render(request, "registration/register_done.html", None)


@csrf_protect
def check_email(request):
    try:
        u = User.objects.get(email__exact=(request.POST['email']))
        return JsonResponse({'stat': 1})  # Erreur si email deja utilise
    except User.DoesNotExist:
        return JsonResponse({'stat': 0})


def auth_login(request, email, password):
    from django.contrib.auth import get_user_model, authenticate, login
    if request.method == "POST":
        usr = authenticate(request=request, email=email, password=password)
        if usr is not None:
            if login(request, usr):
                return JsonResponse({'status': 0, 'user': 1})
                pass
            else:
                return JsonResponse({'status': -1})
                pass
            pass
        else:
            return JsonResponse({'status': -1})
            pass
    else:
        return JsonResponse({'status': -1})


