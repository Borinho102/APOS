# Generated by Django 2.2.4 on 2019-11-07 13:23

import Concours.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='APOSBranch',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=96, verbose_name='Nom du Parcours')),
                ('code', models.CharField(blank=True, max_length=8, verbose_name='Code du Parcours')),
                ('place', models.IntegerField(verbose_name='Nombre de places')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('status', models.BooleanField(default=True, help_text='Actif', verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Parcours - APOS',
                'verbose_name_plural': 'Parcours - APOS',
                'db_table': 'apos_branch',
            },
        ),
        migrations.CreateModel(
            name='APOSCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Categorie')),
                ('libelle', models.CharField(max_length=96, verbose_name='Libelle')),
                ('code', models.CharField(max_length=16, verbose_name='Code')),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Categorie Etablissement - APOS',
                'verbose_name_plural': 'Categories Etablissement - APOS',
                'db_table': 'apos_categorie',
            },
        ),
        migrations.CreateModel(
            name='APOSCountry',
            fields=[
                ('id', models.BigAutoField(db_index=True, primary_key=True, serialize=False, unique=True, verbose_name='ID du pays')),
                ('name', models.CharField(max_length=128, verbose_name='Nom du pays')),
                ('code', models.CharField(max_length=4, verbose_name='Code du pays')),
                ('status', models.BooleanField(default=True, verbose_name='Activité du pays')),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
            ],
            options={
                'verbose_name': 'Pays - APOS',
                'verbose_name_plural': 'Pays - APOS',
                'db_table': 'apos_country',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='APOSCursus',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=96, verbose_name='Nom du Cursus')),
                ('code', models.CharField(blank=True, max_length=8, verbose_name='Code du Cursus')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('status', models.BooleanField(default=True, help_text='Actif', verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Cursus - APOS',
                'verbose_name_plural': 'Cursus - APOS',
                'db_table': 'apos_cursus',
            },
        ),
        migrations.CreateModel(
            name='APOSCycle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Cycle')),
                ('libelle', models.CharField(max_length=96, verbose_name='Libelle')),
                ('code', models.CharField(max_length=16, verbose_name='Code du cycle')),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Cycle - APOS',
                'verbose_name_plural': 'Cycles - APOS',
                'db_table': 'apos_cycle',
            },
        ),
        migrations.CreateModel(
            name='APOSDiplome',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=96, verbose_name='Nom du Diplome')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('status', models.BooleanField(default=True, help_text='Actif', verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Diplome - APOS',
                'verbose_name_plural': 'Diplomes - APOS',
                'db_table': 'apos_diplome',
            },
        ),
        migrations.CreateModel(
            name='APOSDomain',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=96, verbose_name='Nom du Domaine')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('status', models.BooleanField(default=True, help_text='Actif', verbose_name='Actif')),
            ],
            options={
                'verbose_name': "Domaine d'etude - APOS",
                'verbose_name_plural': "Domaines d'etude - APOS",
                'db_table': 'apos_domain',
            },
        ),
        migrations.CreateModel(
            name='APOSExam',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID du Concours')),
                ('libelle', models.CharField(max_length=128, verbose_name='Libelle du Concours')),
                ('age_min', models.IntegerField(verbose_name='Age Minimal')),
                ('age_max', models.IntegerField(verbose_name='Age Maximal')),
                ('dossier', models.TextField(blank=True, verbose_name='Composition de dossiers')),
                ('resultat', models.FileField(blank=True, upload_to='Resultat/', verbose_name='Fiche de Resultat')),
                ('date_o', models.DateField(verbose_name="Date d'ouverture")),
                ('date_l', models.DateField(help_text='Limite de depot dossiers', verbose_name='Date limite')),
                ('date_c', models.DateField(verbose_name='Date du Concours')),
                ('date_e', models.DateField(blank=True, verbose_name="Date d'Entretien")),
                ('date_f', models.DateField(blank=True, verbose_name='Date de Cloture')),
                ('encours', models.BooleanField(default=True, verbose_name='En cours')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
            ],
            options={
                'verbose_name': 'Concours - APOS',
                'verbose_name_plural': 'Concours - APOS',
                'db_table': 'apos_concours',
                'ordering': ['cycle'],
            },
        ),
        migrations.CreateModel(
            name='APOSExamCenter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Centre')),
                ('addr', models.CharField(max_length=96, verbose_name='Adresse du centre')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=True, verbose_name='Actif')),
                ('pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSCountry')),
            ],
            options={
                'verbose_name': "Centre d'examen - APOS",
                'verbose_name_plural': "Centres d'examen - APOS",
                'db_table': 'apos_exam_center',
            },
        ),
        migrations.CreateModel(
            name='APOSInterdit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Type')),
                ('libelle', models.CharField(max_length=96, verbose_name='Libelle')),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Statut Interdit - APOS',
                'verbose_name_plural': 'Statuts Interdits - APOS',
                'db_table': 'apos_statut_interdit',
            },
        ),
        migrations.CreateModel(
            name='APOSLieuDepot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Lieu de Depot')),
                ('addr', models.CharField(max_length=96, verbose_name='Adresse du lieu')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=True, verbose_name='Actif')),
                ('pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSCountry')),
            ],
            options={
                'verbose_name': 'Lieu de Depot - APOS',
                'verbose_name_plural': 'Lieux de Depot - APOS',
                'db_table': 'apos_lieu_depot',
            },
        ),
        migrations.CreateModel(
            name='APOSMinistry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Nom du Ministere')),
                ('sigle', models.CharField(max_length=16, verbose_name='Code du Ministere')),
                ('status', models.BooleanField()),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSCountry')),
            ],
            options={
                'verbose_name': 'Ministère - APOS',
                'verbose_name_plural': 'Ministères - APOS',
                'db_table': 'apos_ministry',
            },
        ),
        migrations.CreateModel(
            name='APOSPaymentAPI',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('service', models.CharField(max_length=64, verbose_name='Nom du Service')),
                ('company', models.CharField(default='', max_length=64, verbose_name='Nom du Service')),
                ('logo', models.ImageField(blank=True, upload_to='Partner/', verbose_name='Logo du Service')),
                ('client_key', models.CharField(blank=True, max_length=128, verbose_name='Clé publique Client')),
                ('client_secret', models.CharField(blank=True, max_length=128, verbose_name='Clé privée Client')),
                ('api_key', models.TextField(blank=True, verbose_name='Clé API')),
                ('status', models.BooleanField(default=False, verbose_name='Actif')),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
            ],
            options={
                'verbose_name': 'API Paiement - APOS',
                'verbose_name_plural': 'APIs Paiement - APOS',
                'db_table': 'apos_payment_api',
            },
        ),
        migrations.CreateModel(
            name='APOSPrice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pack', models.CharField(max_length=64, verbose_name="Pack d'abonnement")),
                ('min_val', models.IntegerField(default=0, verbose_name='Nombre min. de concours')),
                ('max_val', models.IntegerField(default=0, verbose_name='Nombre max. de concours')),
                ('prix_sms', models.IntegerField(verbose_name='Prix des SMS Alerte')),
                ('prix_end', models.IntegerField(help_text="SMS d'annonce de fin d'abonnement", verbose_name='Prix du SMS')),
                ('prix_ver', models.IntegerField(verbose_name='Prix du SMS Verification')),
                ('prix_mail', models.IntegerField(verbose_name='Prix des Mails Alerte')),
            ],
            options={
                'verbose_name': 'Prix - APOS',
                'verbose_name_plural': 'Prix - APOS',
                'db_table': 'apos_price',
            },
        ),
        migrations.CreateModel(
            name='APOSStatut',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Type')),
                ('libelle', models.CharField(max_length=96, verbose_name='Libelle')),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
            ],
            options={
                'verbose_name': 'Statut - APOS',
                'verbose_name_plural': 'Statuts - APOS',
                'db_table': 'apos_statut',
            },
        ),
        migrations.CreateModel(
            name='APOSUserPay',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rest_sms', models.IntegerField(default=0, verbose_name='SMS Restant')),
                ('rest_mail', models.IntegerField(default=0, verbose_name='Mail Restant')),
                ('status', models.BooleanField(default=False, verbose_name='Actif')),
                ('reg_date', models.DateField(auto_now_add=True, verbose_name="Date d'abonnement")),
                ('exams', models.ManyToManyField(related_name='abonne', to='Concours.APOSExam')),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSPrice')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Abonnement - APOS',
                'verbose_name_plural': 'Abonnements - APOS',
                'db_table': 'apos_user_payment',
            },
        ),
        migrations.CreateModel(
            name='APOSUniversite',
            fields=[
                ('id', models.CharField(db_index=True, default=Concours.models.createUnivID, editable=False, max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Identifiant Université')),
                ('name', models.CharField(max_length=64, verbose_name="Nom de l'Université")),
                ('sigle', models.CharField(db_index=True, max_length=8, unique=True, verbose_name="Sigle de l'Université")),
                ('logo', models.ImageField(blank=True, upload_to='Universite/', verbose_name='Logo')),
                ('priorite', models.BigIntegerField(default=0, verbose_name="Priorité de l'établissement")),
                ('tag', models.TextField(blank=True, db_index=True, help_text='Utile pour des recherches rapides', verbose_name='Liste des index')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name="Email de l'établissement")),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, verbose_name="Telephone de l'établissement")),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, verbose_name="Fax de l'établissement")),
                ('web', models.URLField(blank=True, verbose_name="Lien site web de l'établissement")),
                ('inscription', models.URLField(blank=True, verbose_name="Lien d'inscription de l'établissement")),
                ('pobox', models.CharField(blank=True, max_length=32, verbose_name="Boite postale de l'établissement")),
                ('status', models.BooleanField(default=True, help_text="Activité de l'etablissement", verbose_name='Actif')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('delivre', models.ManyToManyField(to='Concours.APOSDiplome')),
                ('pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSCountry')),
                ('tutelle', models.ManyToManyField(to='Concours.APOSMinistry')),
                ('type', models.ForeignKey(help_text="Statut de l'établissement", on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSStatut')),
            ],
            options={
                'verbose_name': 'Université - APOS',
                'verbose_name_plural': 'Universités - APOS',
                'db_table': 'apos_university',
            },
        ),
        migrations.CreateModel(
            name='APOSSchools',
            fields=[
                ('id', models.CharField(db_index=True, default=Concours.models.createSchoolID, editable=False, max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Identifiant Etablissement')),
                ('name', models.CharField(max_length=64, verbose_name="Nom de l'Etablissement")),
                ('sigle', models.CharField(db_index=True, max_length=8, unique=True, verbose_name="Sigle de l'Etablissement")),
                ('logo', models.ImageField(blank=True, upload_to='Etablissement/', verbose_name='Logo')),
                ('priorite', models.BigIntegerField(default=0, verbose_name="Priorité de l'établissement")),
                ('tag', models.TextField(blank=True, db_index=True, help_text='Utile pour des recherches rapides', verbose_name='Liste des index')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name="Email de l'établissement")),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, verbose_name="Telephone de l'établissement")),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, verbose_name="Fax de l'établissement")),
                ('web', models.URLField(blank=True, verbose_name="Lien site web de l'établissement")),
                ('inscription', models.URLField(blank=True, verbose_name="Lien d'inscription de l'établissement")),
                ('pobox', models.CharField(blank=True, max_length=32, verbose_name="Boite postale de l'établissement")),
                ('status', models.BooleanField(default=True, help_text="Activité de l'etablissement", verbose_name='Actif')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('category', models.ForeignKey(help_text="Type d'établissement", on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSCategory')),
                ('centre', models.ManyToManyField(to='Concours.APOSExamCenter')),
                ('delivre', models.ManyToManyField(to='Concours.APOSDiplome')),
                ('lieu', models.ManyToManyField(to='Concours.APOSLieuDepot')),
                ('statut', models.ForeignKey(help_text="Statut de l'établissement", on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSStatut')),
                ('tutelle', models.ManyToManyField(to='Concours.APOSMinistry')),
                ('universite', models.ForeignKey(help_text='Sous-Tutelle Universitaire', on_delete=django.db.models.deletion.CASCADE, related_name='school_universite', to='Concours.APOSUniversite')),
            ],
            options={
                'verbose_name': 'Etablissement - APOS',
                'verbose_name_plural': 'Etablissements - APOS',
                'db_table': 'apos_school',
            },
        ),
        migrations.CreateModel(
            name='APOSReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name="Téléphone d'abonnement")),
                ('pay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSPaymentAPI')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSUserPay')),
            ],
            options={
                'verbose_name': 'Facture - APOS',
                'verbose_name_plural': 'Factures - APOS',
                'db_table': 'apos_payment_receipt',
            },
        ),
        migrations.CreateModel(
            name='APOSLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Niveau')),
                ('libelle', models.CharField(max_length=96, verbose_name='Libelle')),
                ('date', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('cursus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSCursus')),
            ],
            options={
                'verbose_name': 'Niveau - APOS',
                'verbose_name_plural': 'Niveaux - APOS',
                'db_table': 'apos_level',
            },
        ),
        migrations.CreateModel(
            name='APOSExamCourse',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=96, verbose_name='Nom de la matière')),
                ('date', models.DateField(verbose_name='Date de Passage')),
                ('heure', models.TimeField(verbose_name='Heure de Passage')),
                ('duree', models.IntegerField(verbose_name='Duree en heures')),
                ('coef', models.FloatField(verbose_name='Coefficient')),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('status', models.BooleanField(default=True, help_text='Actif', verbose_name='Actif')),
                ('concours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSBranch')),
            ],
            options={
                'verbose_name': 'Matière Concours - APOS',
                'verbose_name_plural': 'Matières Concours - APOS',
                'db_table': 'apos_exam_course',
            },
        ),
        migrations.AddField(
            model_name='aposexam',
            name='concours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSLevel'),
        ),
        migrations.AddField(
            model_name='aposexam',
            name='cycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSCycle'),
        ),
        migrations.AddField(
            model_name='aposexam',
            name='interdit',
            field=models.ManyToManyField(to='Concours.APOSInterdit'),
        ),
        migrations.AddField(
            model_name='aposdiplome',
            name='domain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Concours.APOSDomain'),
        ),
        migrations.AddField(
            model_name='aposdiplome',
            name='pays',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSCountry'),
        ),
        migrations.AddField(
            model_name='aposcursus',
            name='etablissement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSSchools'),
        ),
        migrations.CreateModel(
            name='APOSCourse',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=96, verbose_name='Nom de la matière')),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('status', models.BooleanField(default=True, help_text='Actif', verbose_name='Actif')),
                ('concours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSBranch')),
            ],
            options={
                'verbose_name': 'Matire Potentielle - APOS',
                'verbose_name_plural': 'Matières Potentielles - APOS',
                'db_table': 'apos_course',
            },
        ),
        migrations.AddField(
            model_name='aposbranch',
            name='concours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSExam'),
        ),
        migrations.AddField(
            model_name='aposbranch',
            name='domaine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Concours.APOSDomain'),
        ),
        migrations.AddField(
            model_name='aposbranch',
            name='requis',
            field=models.ManyToManyField(to='Concours.APOSDiplome'),
        ),
    ]
