from django.contrib import admin

from .models import ReceivedMessage


class ReceivedMessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(ReceivedMessage, ReceivedMessageAdmin)
