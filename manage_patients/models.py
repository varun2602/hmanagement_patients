from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import uuid



# Create your models here.
class Patient(AbstractUser):
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)

    PatientID = models.CharField(max_length=10, primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_designation = models.CharField(max_length=100, blank=True, null=True)
    work_hours_start = models.TimeField(default=datetime.time(9, 0))
    work_hours_end = models.TimeField(default=datetime.time(17, 0))
    insurance = models.CharField(max_length=50, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_groups1', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions1', blank=True
    )

    

    def __str__(self):
        return f"Patient: {self.username}"
