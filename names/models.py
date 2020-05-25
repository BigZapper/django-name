from django.db import models


class Name(models.Model):
    fullname = models.CharField(max_length=255, blank=False, default='')
    menh = models.CharField(max_length=255,blank=False, default='')
    van = models.CharField(max_length=255,blank=False, default='')
    gioitinh = models.CharField(max_length=255,blank=False, default='')
    lastname = models.CharField(max_length=255,blank=False, default='')
    meaning = models.CharField(max_length=1024,blank=True, default='')
