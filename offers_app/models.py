from django.db import models

class Offer(models.Model):
    title = models.CharField(max_length=50)
    image = models.FileField(upload_to="media/", blank=True, null=True)
    description = models.CharField(max_length=255)

class OfferDetail(models.Model):
    title = models.CharField(max_length=50)
    revisions = models.IntegerField()