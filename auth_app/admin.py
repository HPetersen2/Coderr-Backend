from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import UserProfile

class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile
        exclude = ('get_display_name',)

@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    resource_class = UserProfileResource
