#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
#from django.contrib.auth.models import User
from django.contrib import messages
from forms import SendForm
from . import models as m

import os
APP_NAME = os.path.split(os.path.dirname(__file__))[-1]


def home(request):
    if request.method == 'GET':
        form = SendForm()
    else:
        form = SendForm(request.POST)
        if form.is_valid():
            send = form.save()
            send.do()
            messages.success(request,'发送成功!')
            return redirect('home')

    ctx = {'form':form}
    ctx['objs'] = m.Tmail.objects.all()
    return render(request,'home.html',ctx)

def preview(request,pk):
    tmail = get_object_or_404(m.Tmail,pk=pk)
    return render(request,tmail.tpath())
