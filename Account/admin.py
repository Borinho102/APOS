from django.contrib import admin
from Account.models import *


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ('uid', 'user')
    list_display = ('uid', 'user',)
    readonly_fields = ('uid',)
    filter_horizontal = ('diplome',)


admin.site.register(UserData, UserAdmin)
