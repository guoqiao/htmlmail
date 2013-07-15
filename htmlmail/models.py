#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import threading
from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from mailer.engine import send_all

class Tmail(models.Model):
    title = models.CharField('邮件标题',max_length=60)
    reply = models.EmailField('回复到')
    tname  = models.CharField('模板名称',max_length=30)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title or self.tname

    def tpath(self):
        return 'mail/%s.html' % self.tname

    def html_content(self):
        return render_to_string(self.tpath())

    def text_content(self):
        return 'TODO'

class Mailer(threading.Thread):

    def run(self):
        print 'send all in thread begin...'
        send_all()
        print 'send all in thread done...'

class Send(models.Model):
    tmail = models.ForeignKey(Tmail,verbose_name='邮件模板')
    title = models.CharField('邮件标题',max_length=60)
    reply = models.EmailField('回复到')
    tname  = models.CharField('模板名称',max_length=30)
    mails = models.TextField('收件人',max_length=2048,blank=True)
    status = models.CharField('状态',max_length=10,default='todo')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.pk:
            # info backup
            self.title = self.tmail.title
            self.reply = self.tmail.reply
            self.tname = self.tmail.tname
        super(Send,self).save(*args,**kwargs)

    def do(self):
        from_email = settings.EMAIL_HOST_USER
        tmail = self.tmail
        total = 0
        success = 0
        for mail in self.mails.split(','):
            total += 1
            try:
                msg = EmailMultiAlternatives(
                        tmail.title,
                        tmail.text_content(),
                        from_email,
                        [mail],
                        #headers = {'Reply-To': tmail.reply}
                    )
                msg.attach_alternative(tmail.html_content(), "text/html")
                print 'sending mail to %s' % mail
                msg.send()
                success += 1
            except:
                print 'sending fail: %s' % mail
                continue
        self.status = 'done'
        self.save()
        if settings.EMAIL_SEND_NOW:
            mailer = Mailer()
            mailer.start()
        return total,success

