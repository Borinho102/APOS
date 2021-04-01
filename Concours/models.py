from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from Orientation.models import *
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from djongo.models.fields import EmbeddedModelField
from random import randint
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

def createUnivID():
    x = ''
    for i in range(16):
        x += str(randint(0, 9))
    try:
        APOSUniversite.objects.get(id=x)
        return createSchoolID()
    except APOSUniversite.DoesNotExist:
        return x


def createSchoolID():
    x = ''
    for i in range(16):
        x += str(randint(0, 9))
    try:
        APOSSchools.objects.get(id=x)
        return createSchoolID()
    except APOSSchools.DoesNotExist:
        return x


class APOSInterdit(models.Model):
    id = models.AutoField(_("ID Type"), primary_key=True)
    libelle = models.CharField(_("Libelle"), max_length=96)
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)
    actif = models.BooleanField(_("Actif"), default=True)

    class Meta:
        db_table = "apos_statut_interdit"
        verbose_name = "Statut Interdit - APOS"
        verbose_name_plural = "Statuts Interdits - APOS"

    def __str__(self):
        return self.libelle


class APOSStatut(models.Model):
    id = models.AutoField(_("ID Type"), primary_key=True)
    libelle = models.CharField(_("Libelle"), max_length=96)
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)
    actif = models.BooleanField(_("Actif"), default=True)

    class Meta:
        db_table = "apos_statut"
        verbose_name = "Statut - APOS"
        verbose_name_plural = "Statuts - APOS"

    def __str__(self):
        return self.libelle


class APOSCategory(models.Model):
    id = models.AutoField(_("ID Categorie"), primary_key=True)
    libelle = models.CharField(_("Libelle"), max_length=96)
    code = models.CharField(_("Code"), max_length=16)
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)
    actif = models.BooleanField(_("Actif"), default=True)

    class Meta:
        db_table = "apos_categorie"
        verbose_name = "Categorie Etablissement - APOS"
        verbose_name_plural = "Categories Etablissement - APOS"

    def __str__(self):
        return self.libelle


class APOSCycle(models.Model):
    id = models.AutoField(_("ID Cycle"), primary_key=True)
    libelle = models.CharField(_("Libelle"), max_length=96)
    code = models.CharField(_("Code du cycle"), max_length=16)
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)
    actif = models.BooleanField(_("Actif"), default=True)

    class Meta:
        db_table = "apos_cycle"
        verbose_name = "Cycle - APOS"
        verbose_name_plural = "Cycles - APOS"

    def __str__(self):
        return self.libelle


class APOSCountry(models.Model):
    id = models.BigAutoField(_("ID du pays"), primary_key=True, unique=True, db_index=True, editable=True)
    name = models.CharField(_("Nom du pays"), max_length=128)
    code = models.CharField(_("Code du pays"), max_length=4)
    status = models.BooleanField(_("Activité du pays"), default=True)
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)

    class Meta:
        db_table = "apos_country"
        verbose_name = _("Pays - APOS")
        verbose_name_plural = _("Pays - APOS")
        ordering = ['date']

    def __str__(self):
        return "{0}({1})".format(self.name, self.code)

    pass


class APOSMinistry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_("Nom du Ministere"), max_length=128, blank=False)
    sigle = models.CharField(_("Code du Ministere"), max_length=16, blank=False)
    pays = models.ForeignKey(APOSCountry, on_delete=models.CASCADE)
    status = models.BooleanField()
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)

    class Meta:
        db_table = "apos_ministry"
        verbose_name = _("Ministère - APOS")
        verbose_name_plural = _("Ministères - APOS")

    @property
    def country(self):
        return self.pays.name

    def __str__(self):
        return "{0}({1})".format(self.sigle, self.pays.code)


class APOSDomain(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_('Nom du Domaine'), max_length=96)
    date = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    status = models.BooleanField(_("Actif"), default=True, help_text=_("Actif"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "apos_domain"
        verbose_name = _("Domaine d'etude - APOS")
        verbose_name_plural = _("Domaines d'etude - APOS")

    pass


class APOSDiplome(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_('Nom du Diplome'), max_length=96)
    date = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    status = models.BooleanField(_("Actif"), default=True, help_text=_("Actif"))
    pays = models.ForeignKey(APOSCountry, on_delete=models.CASCADE)
    domain = models.ForeignKey(APOSDomain, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    @property
    def domaine(self):
        return self.domain.name

    @property
    def country(self):
        return self.pays.name

    class Meta:
        db_table = "apos_diplome"
        verbose_name = _("Diplome - APOS")
        verbose_name_plural = _("Diplomes - APOS")

    pass


class APOSUniversite(models.Model):
    id = models.CharField(_("Identifiant Université"), primary_key=True, unique=True, db_index=True, max_length=20,
                          default=createUnivID, editable=False)
    name = models.CharField(_("Nom de l'Université"), max_length=64)
    sigle = models.CharField(_("Sigle de l'Université"), max_length=8, unique=True, db_index=True)
    logo = models.ImageField(_("Logo"), upload_to="Universite/", blank=True)

    pays = models.ForeignKey(APOSCountry, on_delete=models.CASCADE)
    type = models.ForeignKey(APOSStatut, help_text=_("Statut de l'établissement"), on_delete=models.CASCADE)

    priorite = models.BigIntegerField(_("Priorité de l'établissement"), default=0)
    tag = models.TextField(_("Liste des index"), blank=True, db_index=True,
                           help_text=_("Utile pour des recherches rapides"))

    email = models.EmailField(_("Email de l'établissement"), blank=True)
    phone = PhoneNumberField(_("Telephone de l'établissement"), blank=True)
    fax = PhoneNumberField(_("Fax de l'établissement"), blank=True)
    web = models.URLField(_("Lien site web de l'établissement"), blank=True)
    inscription = models.URLField(_("Lien d'inscription de l'établissement"), blank=True)
    pobox = models.CharField(_("Boite postale de l'établissement"), max_length=32, blank=True)

    status = models.BooleanField(_("Actif"), default=True, help_text=_("Activité de l'etablissement"))
    date = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)

    tutelle = models.ManyToManyField(APOSMinistry)
    delivre = models.ManyToManyField(APOSDiplome)

    @property
    def type_univ(self):
        return self.type

    def __str__(self):
        return "{0}({1})".format(self.name, self.pays.code)

    class Meta:
        db_table = "apos_university"
        verbose_name = _("Université - APOS")
        verbose_name_plural = _("Universités - APOS")

    pass


class APOSExamCenter(models.Model):
    id = models.AutoField(_("ID Centre"), primary_key=True)
    addr = models.CharField(_("Adresse du centre"), max_length=96)
    pays = models.ForeignKey(APOSCountry, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(_("Actif"), default=True)

    class Meta:
        db_table = "apos_exam_center"
        verbose_name = _("Centre d'examen - APOS")
        verbose_name_plural = _("Centres d'examen - APOS")

    @property
    def country(self):
        return self.pays.name

    def __str__(self):
        return "{0}({1})".format(self.addr, self.pays.name)


class APOSLieuDepot(models.Model):
    id = models.AutoField(_("ID Lieu de Depot"), primary_key=True)
    addr = models.CharField(_("Adresse du lieu"), max_length=96)
    pays = models.ForeignKey(APOSCountry, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(_("Actif"), default=True)

    @property
    def country(self):
        return self.pays.name

    class Meta:
        db_table = "apos_lieu_depot"
        verbose_name = _("Lieu de Depot - APOS")
        verbose_name_plural = _("Lieux de Depot - APOS")

    def __str__(self):
        return "{0}({1})".format(self.addr, self.pays.name)


class APOSSchools(models.Model):
    id = models.CharField(_("Identifiant Etablissement"), primary_key=True, unique=True, db_index=True, max_length=20,
                          default=createSchoolID, editable=False)
    name = models.CharField(_("Nom de l'Etablissement"), max_length=64)
    sigle = models.CharField(_("Sigle de l'Etablissement"), max_length=8, unique=True, db_index=True)
    logo = models.ImageField(_("Logo"), upload_to="Etablissement/", blank=True)

    universite = models.ForeignKey(APOSUniversite, on_delete=models.CASCADE, related_name="school_universite",
                                   help_text=_('Sous-Tutelle Universitaire'))

    statut = models.ForeignKey(APOSStatut, on_delete=models.CASCADE, help_text=_("Statut de l'établissement"))
    category = models.ForeignKey(APOSCategory, on_delete=models.CASCADE, help_text=_("Type d'établissement"))

    priorite = models.BigIntegerField(_("Priorité de l'établissement"), default=0)
    tag = models.TextField(_("Liste des index"), blank=True, db_index=True, help_text=_("Utile pour des recherches "
                                                                                        "rapides"))

    email = models.EmailField(_("Email de l'établissement"), blank=True)
    phone = PhoneNumberField(_("Telephone de l'établissement"), blank=True)
    fax = PhoneNumberField(_("Fax de l'établissement"), blank=True)
    web = models.URLField(_("Lien site web de l'établissement"), blank=True)
    inscription = models.URLField(_("Lien d'inscription de l'établissement"), blank=True)
    pobox = models.CharField(_("Boite postale de l'établissement"), max_length=32, blank=True)

    status = models.BooleanField(_("Actif"), default=True, help_text=_("Activité de l'etablissement"))
    date = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)

    tutelle = models.ManyToManyField(APOSMinistry)
    delivre = models.ManyToManyField(APOSDiplome)
    lieu = models.ManyToManyField(APOSLieuDepot)
    centre = models.ManyToManyField(APOSExamCenter)

    @property
    def type_etab(self):
        return self.statut.libelle

    @property
    def univ_etab(self):
        return self.universite.name

    @property
    def category_etab(self):
        return self.category.libelle

    def __str__(self):
        return "{0}({1} - {2})".format(self.name, self.universite.sigle, self.universite.pays.code)

    class Meta:
        db_table = "apos_school"
        verbose_name = _("Etablissement - APOS")
        verbose_name_plural = _("Etablissements - APOS")

    pass


class APOSCursus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_('Nom du Cursus'), max_length=96)
    code = models.CharField(_('Code du Cursus'), max_length=8, blank=True)
    date = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    status = models.BooleanField(_("Actif"), default=True, help_text=_("Actif"))
    etablissement = models.ForeignKey(APOSSchools, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}({1})".format(self.name, self.etablissement.sigle)

    @property
    def school(self):
        return self.etablissement.name

    class Meta:
        db_table = "apos_cursus"
        verbose_name = _("Cursus - APOS")
        verbose_name_plural = _("Cursus - APOS")

    pass


class APOSLevel(models.Model):
    id = models.AutoField(_("ID Niveau"), primary_key=True)
    libelle = models.CharField(_("Libelle"), max_length=96)
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)
    actif = models.BooleanField(_("Actif"), default=True)
    cursus = models.ForeignKey(APOSCursus, on_delete=models.CASCADE)

    class Meta:
        db_table = "apos_level"
        verbose_name = "Niveau - APOS"
        verbose_name_plural = "Niveaux - APOS"

    @property
    def parcours(self):
        return self.cursus.name

    def __str__(self):
        return "{0}-{1}[{2}]".format(self.cursus.etablissement.sigle, self.cursus.code, self.libelle)


from django.db.models.signals import pre_save


class APOSExam(models.Model):
    id = models.BigAutoField(_("ID du Concours"), primary_key=True)
    libelle = models.CharField(_("Libelle du Concours"), max_length=128)
    concours = models.ForeignKey(APOSLevel, on_delete=models.CASCADE)
    cycle = models.ForeignKey(APOSCycle, on_delete=models.CASCADE)

    age_min = models.IntegerField(_("Age Minimal"))
    age_max = models.IntegerField(_("Age Maximal"))
    interdit = models.ManyToManyField(APOSInterdit)
    dossier = models.TextField(_("Composition de dossiers"), blank=True)
    resultat = models.FileField(_("Fiche de Resultat"), upload_to="Resultat/", blank=True)

    date_o = models.DateField(_("Date d'ouverture"))
    date_l = models.DateField(_("Date limite"), help_text=_("Limite de depot dossiers"))
    date_c = models.DateField(_("Date du Concours"))
    date_e = models.DateField(_("Date d'Entretien"), blank=True)
    date_f = models.DateField(_("Date de Cloture"), blank=True)

    encours = models.BooleanField(_("En cours"), default=True)
    actif = models.BooleanField(_("Actif"), default=True)
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)

    class Meta:
        db_table = "apos_concours"
        ordering = ['cycle']
        verbose_name = "Concours - APOS"
        verbose_name_plural = "Concours - APOS"

    def __str__(self):
        return "Concours {0}[{1}] {2} - {3} ".format(self.concours.cursus.etablissement.sigle,
                                                     self.concours.cursus.code, self.concours.libelle,
                                                     self.cycle.libelle)


def set_libelle(sender, instance, **kwargs):
    instance.libelle = str(instance.concours) + " | " + instance.cycle.code


pre_save.connect(set_libelle, APOSExam)


class APOSBranch(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_('Nom du Parcours'), max_length=96)
    code = models.CharField(_('Code du Parcours'), max_length=8, blank=True)

    concours = models.ForeignKey(APOSExam, on_delete=models.CASCADE)
    place = models.IntegerField(_("Nombre de places"))
    requis = models.ManyToManyField(APOSDiplome)

    date = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    status = models.BooleanField(_("Actif"), default=True, help_text=_("Actif"))
    domaine = models.ForeignKey(APOSDomain, on_delete=models.CASCADE)

    @property
    def domain(self):
        return self.domaine.name

    def __str__(self):
        return "{0}({1}[{2} - {3}])".format(
            self.name, self.concours.concours.cursus.etablissement.sigle,
            self.concours.concours.libelle, self.concours.concours.cursus.code)

    class Meta:
        db_table = "apos_branch"
        verbose_name = _("Parcours - APOS")
        verbose_name_plural = _("Parcours - APOS")

    pass




class APOSExamCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_('Nom de la matière'), max_length=96)

    date = models.DateField(_('Date de Passage'))
    heure = models.TimeField(_('Heure de Passage'))
    duree = models.IntegerField(_('Duree en heures'))

    # concours = models.ForeignKey(APOSBranch, on_delete=models.CASCADE)
    concours = models.ForeignKey(APOSBranch, on_delete=models.CASCADE)
    coef = models.FloatField(_("Coefficient"))

    date_add = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    status = models.BooleanField(_("Actif"), default=True, help_text=_("Actif"))

    def __str__(self):
        return "{0} - {1}".format(self.name, self.concours)

    class Meta:
        db_table = "apos_exam_course"
        verbose_name = _("Matière Concours - APOS")
        verbose_name_plural = _("Matières Concours - APOS")


class APOSCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_('Nom de la matière'), max_length=96)
    concours = models.ForeignKey(APOSBranch, on_delete=models.CASCADE)
    date_add = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    status = models.BooleanField(_("Actif"), default=True, help_text=_("Actif"))

    def __str__(self):
        return "{0} - {1}".format(self.name, self.concours)

    class Meta:
        db_table = "apos_course"
        verbose_name = _("Matire Potentielle - APOS")
        verbose_name_plural = _("Matières Potentielles - APOS")


# Create your models here.

class APOSPaymentAPI(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    service = models.CharField(_("Nom du Service"), max_length=64)
    company = models.CharField(_("Nom du Service"), max_length=64, default="")
    logo = models.ImageField(_("Logo du Service"), upload_to='Partner/', blank=True)
    client_key = models.CharField(_("Clé publique Client"), max_length=128, blank=True)
    client_secret = models.CharField(_("Clé privée Client"), max_length=128, blank=True)
    api_key = models.TextField(_("Clé API"), blank=True)
    status = models.BooleanField(_("Actif"), default=False)
    date = models.DateField(_("Date d'ajout"), auto_now_add=True)

    class Meta:
        db_table = "apos_payment_api"
        verbose_name = _("API Paiement - APOS")
        verbose_name_plural = _("APIs Paiement - APOS")

    def __str__(self):
        return self.service

    pass


class APOSPrice(models.Model):
    id = models.AutoField(primary_key=True)
    pack = models.CharField(_("Pack d'abonnement"), max_length=64)
    min_val = models.IntegerField(_('Nombre min. de concours'), default=0)
    max_val = models.IntegerField(_('Nombre max. de concours'), default=0)
    prix_sms = models.IntegerField(_('Prix des SMS Alerte'))
    prix_end = models.IntegerField(_('Prix du SMS'), help_text=_("SMS d'annonce de fin d'abonnement"))
    prix_ver = models.IntegerField(_('Prix du SMS Verification'))
    prix_mail = models.IntegerField(_('Prix des Mails Alerte'))

    class Meta:
        db_table = "apos_price"
        verbose_name = _("Prix - APOS")
        verbose_name_plural = _("Prix - APOS")

    def __str__(self):
        return self.pack

    pass


class APOSUserPay(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pack = models.ForeignKey(APOSPrice, on_delete=models.CASCADE)
    exams = models.ManyToManyField(APOSExam, related_name="abonne")
    rest_sms = models.IntegerField(_('SMS Restant'), default=0)
    rest_mail = models.IntegerField(_('Mail Restant'), default=0)
    status = models.BooleanField(_("Actif"), default=False)
    reg_date = models.DateField(_("Date d'abonnement"), auto_now_add=True)

    class Meta:
        db_table = "apos_user_payment"
        verbose_name = _("Abonnement - APOS")
        verbose_name_plural = _("Abonnements - APOS")

    def __str__(self):
        return self.user.username

    pass


class APOSReceipt(models.Model):
    number = PhoneNumberField(_("Téléphone d'abonnement"))
    pid = models.ForeignKey(APOSUserPay, on_delete=models.CASCADE)
    pay = models.ForeignKey(APOSPaymentAPI, on_delete=models.CASCADE)

    class Meta:
        db_table = "apos_payment_receipt"
        verbose_name = _("Facture - APOS")
        verbose_name_plural = _("Factures - APOS")

    def __str__(self):
        return self.pid.user.username

    pass


e_reason = models.CharField(max_length=64)
