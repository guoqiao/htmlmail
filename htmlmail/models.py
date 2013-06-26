#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

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
        for mail in self.mails.split(','):
            msg = EmailMultiAlternatives(
                    tmail.title,
                    tmail.text_content(),
                    from_email,
                    [mail],
                    headers = {'Reply-To': tmail.reply}
                )
            msg.attach_alternative(tmail.html_content(), "text/html")
            print 'sending mail to %s' % mail
            msg.send()
        self.status = 'done'
        self.save()

