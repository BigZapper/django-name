from django.db import models
from django.contrib.auth import get_user_model


class Name(models.Model):
    fullname = models.CharField(max_length=255, blank=False, default='')
    menh = models.CharField(max_length=255,blank=False, default='')
    van = models.CharField(max_length=255,blank=False, default='')
    gioitinh = models.CharField(max_length=255,blank=False, default='')
    lastname = models.CharField(max_length=255,blank=False, default='')
    meaning = models.CharField(max_length=1024,blank=True, default='')
    thanh = models.CharField(max_length=255,blank=True,default='')
    likes = models.IntegerField(default=0)


class MidName(models.Model):
    tenlot = models.CharField(max_length=255, blank=True, default='')
    menh = models.CharField(max_length=255,blank=True, default='')
    gioitinh = models.CharField(max_length=255,blank=True, default='')
    meaning = models.TextField()
    thanh = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.tenlot
    def __meaning__(self):
        return self.meaning
    def __gender__(self):
        return self.gioitinh
    def __id__(self):
        return self.id    