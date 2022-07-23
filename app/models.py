from django.db import models

# Create your models here.


class apirates(models.Model):
    ip_address = models.TextField(null=False)
    url = models.TextField(null=False, blank=False)
    count = models.IntegerField(default=0)
    lastupdated = models.DateTimeField(auto_now_add=True, blank=True)
    maxrate = models.IntegerField(default=10)

    def __str__(self):
        return self.ip_address
