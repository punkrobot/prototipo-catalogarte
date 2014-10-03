from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from webapp.models import Museo

class MuseoInline(admin.StackedInline):
    model = Museo
    can_delete = False

class MuseoAdmin(UserAdmin):
    inlines = (MuseoInline, )

admin.site.unregister(User)
admin.site.register(User, MuseoAdmin)
