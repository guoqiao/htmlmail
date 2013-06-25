#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.shortcuts import render,redirect
#from django.shortcuts import get_object_or_404
#from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from forms import SendForm

import os
APP_NAME = os.path.split(os.path.dirname(__file__))[-1]

def get_mails(text):
    r = re.compile(r'([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
    results = r.findall(text)
    mails = set([])
    for match in results:
        m = match[0]
        if m not in mails:
            mails.add(m)
            print 'match mail:',m
        else:
            print 'skip repteated mail:',m
    return mails

def home(request):
    if request.method == 'GET':
        initial={
                'to':'guoqiao@insigma.com.cn',
                'reply_to':settings.EMAIL_REPLY_TO,
                }
        form = SendForm(initial)
    else:
        form = SendForm(request.POST)
        if form.is_valid():
            to = form.cleaned_data['to'].strip()
            mails = get_mails(to)
            if mails:
                #print mails
                tmpl = form.cleaned_data['tmpl']
                reply_to = form.cleaned_data['reply_to']
                mail_tmpl = 'mail_%s.html' % tmpl
                html_content = render_to_string(mail_tmpl)
                text_content = 'TODO'
                subject = 'hi'
                from_email = settings.EMAIL_HOST_USER
                for mail in mails:
                    msg = EmailMultiAlternatives(
                            subject,
                            text_content,
                            from_email,
                            [mail],
                            headers = {'Reply-To': reply_to}
                        )
                    msg.attach_alternative(html_content, "text/html")
                    print 'sending mail to %s' % mail
                    #msg.send()
                messages.info(request,'发送成功!')
                return redirect('home')

    ctx = {'form':form}
    return render(request,'home.html',ctx)

def preview(request,name):
    tmpl = 'mail_%s.html' % name
    return render(request,tmpl)
