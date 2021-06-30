from django.db import models


class Thing(models.Model):
    color = models.CharField(max_length=255)
