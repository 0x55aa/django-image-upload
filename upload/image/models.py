# coding:utf-8
from django.db import models

class Images(models.Model):
    """
    
    """
    #image_url = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='img/')

