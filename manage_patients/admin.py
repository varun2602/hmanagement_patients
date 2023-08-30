from django.contrib import admin
from . import models 

@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["is_active", "username", "email", "PatientID", "company_name", "company_designation", "work_hours_start", "work_hours_end", "insurance"]
