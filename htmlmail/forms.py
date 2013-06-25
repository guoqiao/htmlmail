#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

TMPLS = (
    ('evernote','evernote'),
    ('hello','hello'),
)

class SendForm(forms.Form):
    tmpl = forms.ChoiceField(label='模板',choices=TMPLS,required=False)
    reply_to = forms.EmailField(label='回复到')
    to = forms.CharField(
            label='收件人',
            max_length=1024,
            widget = forms.Textarea(attrs={"class":"span10"}),
        )
