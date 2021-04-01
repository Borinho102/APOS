from django.db import models
from django.contrib.auth.models import User
from random import randint
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from Concours.models import APOSDiplome


def uid():
    x = ''
    for i in range(25):
        x += str(randint(0, 9))
    try:
        UserData.objects.get(uid=x)
        return uid()
    except UserData.DoesNotExist:
        return x


# Create your models here.

class UserData(models.Model):
    ROLE = (
        ('P', 'Parent'),
        ('E', 'Enfant')
    )
    uid = models.CharField(_('ID Utilisateur'), max_length=32, unique=True, blank=False, default=uid)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_data')
    phone = PhoneNumberField(_('Téléphone'))
    avatar = models.TextField(_('Photo'))
    bdate = models.DateField(_('Date de naissance'))
    diplome = models.ManyToManyField(APOSDiplome)
    role = models.CharField(_('Role'), choices=ROLE, max_length=10, default='E')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'apos_user'
        verbose_name = "User Data"
        verbose_name_plural = "User Data"

    def age(self):
        from datetime import datetime
        return datetime.now().year - self.bdate.year
