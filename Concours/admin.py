from django.contrib import admin
from Concours.models import *
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mass_mail, EmailMessage, EmailMultiAlternatives
from django.core import mail
from Account.models import UserData


# Actions

def locks(modeladmin, request, queryset):
    queryset.update(actif=False)


locks.short_description = _("Désactiver")


def unlocks(modeladmin, request, queryset):
    queryset.update(actif=True)


unlocks.short_description = _("Activer")


def lock(modeladmin, request, queryset):
    queryset.update(status=False)


lock.short_description = _("Désactiver")


def alert(modeladmin, request, queryset):
    import nexmo
    client = nexmo.Client(key="9b9a7a22", secret="Qzmfo9GdocUTy54k")
    conn = mail.get_connection()
    conn.open()
    l = list()
    em = list()
    un = list()
    ph = list()
    for q in queryset:
        e = APOSExam.objects.get(id=q.id)
        b = APOSBranch.objects.filter(concours=e)
        r = APOSUserPay.objects.filter(exams__id=e.id, status=True)
        for i in range(len(r)):
            if r[i].user.email not in l:
                l.append(r[i].user.email)
                un.append(r[i].user.username)
            u = UserData.objects.filter(user_id__exact=r[i].user.id).values('phone')
            if u[0]['phone'] not in ph:
                ph.append(u[0]['phone'])
        for x in range(len(ph)):
            responseData = client.send_message(
                {
                    "from": "APOS Organization",
                    "to": str(ph[x]),
                    "text": "Salut M. " + un[x] + "! Nous vous informons du lancement du concours - " + e.libelle + " lancé le " + str(e.date_o) + ". La date limite de depot des dossiers est"
                            "prevu le " + str(e.date_l) + ".Consultez vos mails ou compte pour plus d'informations.",
                }
            )
            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
            print("")
        for i in l:
            m = EmailMultiAlternatives(
                'Ouverture Concours - Alerte APOS',
                "<div style='background: #4a148c; padding: 25px'><div style='background: #fff; border-radius:7px; padding: 15px; margin: 15px'>"
                "<center><img src='https://127.0.0.1:9595/static/checking.png' width=200 height=200/><br/><br>"
                "Salut, APOS vous informe du <br/><h3><b>"
                "Lancement d'un concours - " + e.libelle + "</b></h3><br/><br/></center><br>"
                "Ce concours a été lancé de " + str(e.date_o) + " et la date limite des dossiers est prevue pour le " + str(e.date_l) + "<br>"
                "<table><table></div></div>",
                'alerte-concours@apos.org',
                [i]
            )
            m.content_subtype = 'html'
            em.append(m)
        print(b)
        conn.send_messages(em)
    conn.close()


alert.short_description = _("Alerter - Ouverture Concours")


def unlock(modeladmin, request, queryset):
    queryset.update(status=True)


unlock.short_description = _("Activer")


# class TypeAdmin(admin.ModelAdmin):
#     search_fields = ('libelle', 'code',)
#     list_display = ('libelle', 'code', 'actif', 'date')
#     actions = [locks, unlocks]
#     list_filter = ('actif',)
#     list_per_page = 10
#     list_display_links = ('libelle',)
#
#
# admin.site.register(APOSType, TypeAdmin)


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('libelle', 'code',)
    list_display = ('libelle', 'code', 'actif', 'date')
    actions = [locks, unlocks]
    list_filter = ('actif',)
    list_per_page = 10
    list_display_links = ('libelle',)


admin.site.register(APOSCategory, CategoryAdmin)


class LevelAdmin(admin.ModelAdmin):
    search_fields = ('libelle',)
    list_display = ('libelle', 'actif', 'date')
    actions = [locks, unlocks]
    list_filter = ('actif',)
    list_per_page = 10
    list_display_links = ('libelle',)


admin.site.register(APOSLevel, LevelAdmin)


class CycleAdmin(admin.ModelAdmin):
    search_fields = ('libelle', 'code',)
    list_display = ('libelle', 'code', 'actif', 'date')
    actions = [locks, unlocks]
    list_filter = ('actif',)
    list_per_page = 10
    list_display_links = ('libelle',)


admin.site.register(APOSCycle, CycleAdmin)


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code',)
    list_display = ('name', 'code', 'status', 'date')
    actions = [lock, unlock]
    list_filter = ('status',)
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSCountry, CountryAdmin)


class MinistryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'sigle',)
    list_display = ('name', 'country', 'sigle', 'status', 'date')
    actions = [lock, unlock]
    list_filter = ('status',)
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSMinistry, MinistryAdmin)


class DomainAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'status', 'date')
    actions = [lock, unlock]
    list_filter = ('status',)
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSDomain, DomainAdmin)


class DiplomeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'domaine',)
    list_display = ('name', 'country', 'domaine', 'status', 'date')
    actions = [lock, unlock]
    list_filter = ('status', 'pays')
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSDiplome, DiplomeAdmin)


class UniversiteAdmin(admin.ModelAdmin):
    search_fields = ('name', 'sigle',)
    list_display = ('name', 'sigle', 'type_univ', 'status', 'date')
    filter_horizontal = ('tutelle', 'delivre',)
    actions = [lock, unlock]
    list_filter = ('status', 'type')
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSUniversite, UniversiteAdmin)


# class DiplomeEntreAdmin(admin.ModelAdmin):
#     search_fields = ('universite', 'diplome',)
#     list_display = ('universites', 'cycle', 'niveau', 'status')
#     actions = [lock, unlock]
#     list_filter = ('niveau', 'status')
#     list_per_page = 10
#     filter_horizontal = ('diplome',)
#     list_display_links = ('universites',)
#
#
# admin.site.register(APOSDiplomeUniversite, DiplomeEntreAdmin)


class ExamCenterAdmin(admin.ModelAdmin):
    search_fields = ('addr',)
    list_display = ('addr', 'status', 'date')
    actions = [locks, unlocks]
    list_filter = ('status',)
    list_per_page = 10
    list_display_links = ('addr',)


admin.site.register(APOSExamCenter, ExamCenterAdmin)


class LieuAdmin(admin.ModelAdmin):
    search_fields = ('addr',)
    list_display = ('addr', 'status', 'date')
    actions = [locks, unlocks]
    list_filter = ('status',)
    list_per_page = 10
    list_display_links = ('addr',)


admin.site.register(APOSLieuDepot, LieuAdmin)


class SchoolAdmin(admin.ModelAdmin):
    search_fields = ('name', 'sigle', 'universite')
    list_display = ('name', 'sigle', 'univ_etab', 'type_etab', 'category_etab', 'status', 'date')
    filter_horizontal = ('tutelle', 'delivre', 'lieu', 'centre')
    actions = [locks, unlocks]
    list_filter = ('status', 'statut', 'category', 'universite')
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSSchools, SchoolAdmin)


class BranchAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code', 'domaine')
    list_display = ('name', 'code', 'concours', 'place', 'status')
    actions = [lock, unlock]
    filter_horizontal = ('requis',)
    list_filter = ('status', 'domaine')
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSBranch, BranchAdmin)


class CursusAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code', 'etablissement')
    list_display = ('name', 'code', 'etablissement', 'status', 'date')
    actions = [lock, unlock]
    list_filter = ('status', 'etablissement')
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSCursus, CursusAdmin)


class ExamCourseAdmin(admin.ModelAdmin):
    search_fields = ('name', 'coef',)
    list_display = ('name', 'concours', 'coef', 'status', 'date_add')
    actions = [lock, unlock]
    list_filter = ('coef', 'status', 'concours')
    list_per_page = 10
    list_display_links = ('name',)


admin.site.register(APOSExamCourse, ExamCourseAdmin)


# class MatiereAdmin(admin.ModelAdmin):
#     search_fields = ('libelle',)
#     list_display = ('libelle', 'code', 'status')
#     actions = [locks, unlocks]
#     list_filter = ('status',)
#     list_per_page = 10
#     list_display_links = ('libelle',)
#
#
# admin.site.register(APOSPotentialCourse, MatiereAdmin)


class ExamAdmin(admin.ModelAdmin):
    search_fields = ('libelle', )
    list_display = ('libelle', 'cycle', 'date_o', 'date_c', 'encours', 'actif')
    list_filter = ('encours', 'cycle', 'age_min', 'age_max', 'concours')
    list_per_page = 10
    actions = [alert]
    list_display_links = ('libelle',)
    filter_horizontal = ('interdit',)


admin.site.register(APOSExam, ExamAdmin)


def lock(modeladmin, request, queryset):
    queryset.update(status=False)


lock.short_description = _("Désactiver")


def unlock(modeladmin, request, queryset):
    queryset.update(status=True)


unlock.short_description = _("Activer")


# Register your models here.

class PayAPIAdmin(admin.ModelAdmin):
    search_fields = ('service',)
    list_display = ('id', 'service', 'company', 'status', 'date')
    actions = [lock, unlock]
    list_filter = ('status',)
    list_per_page = 10
    list_display_links = ('service', 'id')


class PriceAdmin(admin.ModelAdmin):
    actions = [lock, unlock]
    list_display = ('pack', 'min_val', 'max_val', 'prix_sms', 'prix_ver', 'prix_end', 'prix_mail')


class PayAdmin(admin.ModelAdmin):
    actions = [lock, unlock]
    list_display = ('user', 'pack', 'status', 'reg_date')
    list_display_links = ('user',)
    filter_horizontal = ('exams',)
    readonly_fields = ('uid',)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('pid', 'pay')
    list_display_links = ('pid',)


admin.site.register(APOSPaymentAPI, PayAPIAdmin)
admin.site.register(APOSUserPay, PayAdmin)
admin.site.register(APOSPrice, PriceAdmin)
admin.site.register(APOSReceipt, ReceiptAdmin)
admin.site.register(APOSInterdit)
admin.site.register(APOSStatut)
