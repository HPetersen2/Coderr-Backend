from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Offer, OfferDetail

class OfferResource(resources.ModelResource):
    class Meta:
        model = Offer

@admin.register(Offer)
class OfferAdmin(ImportExportModelAdmin):
    resource_class = OfferResource

class OfferDetailResource(resources.ModelResource):
    class Meta:
        model = OfferDetail

@admin.register(OfferDetail)
class OfferDetailAdmin(ImportExportModelAdmin):
    resource_class = OfferDetailResource