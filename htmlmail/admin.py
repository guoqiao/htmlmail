# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from . import models as m

class TmailAdmin(admin.ModelAdmin):
    list_display = ('title','tname','reply','create')
    search_fields = ['title','tname','reply','create']

class SendAdmin(admin.ModelAdmin):
    list_display = ('tmail','mails','status','create')
    search_fields = ['title','tname','reply','mails','status']

admin.site.register(m.Tmail,TmailAdmin)
admin.site.register(m.Send,SendAdmin)
