from django.db import models

# Create your models here.

class puredataset(models.Model):
    year = models.IntegerField(default=2073)
    month = models.IntegerField(default=1)
    day = models.IntegerField(default=1)
    baar = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    eldata = models.FloatField(default=0.0)
    tmdata = models.FloatField(default=0.0)
    hddata = models.FloatField(default=0.0)

