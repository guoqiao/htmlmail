#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django import forms
from .models import Send


class SendForm(forms.ModelForm):
    class Meta:
        model = Send
        fields = ('tmail','mails')

    def clean_mails(self):
        text = self.cleaned_data['mails']
        r = re.compile(r'([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
        matches = r.findall(text)
        mails = set([])
        for match in matches:
            m = match[0]
            if m not in mails:
                mails.add(m)
                print 'match mail:',m
            else:
                print 'skip repteated mail:',m
        return ','.join(mails)

