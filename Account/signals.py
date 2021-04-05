from django.contrib.auth.signals import user_logged_in
from django_registration.signals import user_registered
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
import user_agents
from Account.models import UserData
from ipware.ip import get_real_ip, get_ip
from core.views import csv_creator
from Concours.models import *
# from Orientation.models import *


@receiver(user_logged_in)
def sig_in(sender, user, request, **kwargs):
    ip = get_real_ip(request) or get_ip(request)
    ua = request.META['HTTP_USER_AGENT']
    ua = user_agents.parse(ua)
    try:
        request.session['user_data'] = UserData.objects.filter(user=request.user)[0]
        request.session['browser'] = ua.browser.family
        request.session['navigator'] = ua.browser.family + " " + ua.browser.version_string
        request.session['os'] = ua.os.family + " " + ua.os.version_string
        request.session['platform'] = ua.os.family
    except Exception as e:
        print(str(e))
        pass
    user.last_login = now()
    user.save()
    csv_creator(str(user.id))
    pass


# @receiver(pre_save, sender=APOSExam)
# def update_abonne(sender, instance, **kwargs):
#     instance.num = instance.abonne_lenght
#     pass
