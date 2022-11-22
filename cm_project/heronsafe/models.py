from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Student(models.Model):
    class Vaccined(models.TextChoices):
        FULL = "FULL", _("Fully Vaccinated")
        FIRSTDOSE = "FIRSTDOSE", _("First Dose")
        NEVER = "NEVER", _("Never")

    class Boostered(models.TextChoices):
        FULL = "FULL", _("Fully Boostered")
        FIRSTBOOST = "FIRSTBOOST", _("First Boost")
        NEVER = "NEVER", _("Never")

    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")

    name = models.CharField(max_length=200, null=True)
    student_id = models.CharField(max_length=12, null=True)
    phone = models.CharField(max_length=12, null=True)
    email = models.CharField(max_length=200, primary_key=True)
    birthdate = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True)
    address = models.CharField(max_length=100, null=True)
    is_vaccined = models.CharField(
        max_length=50, choices=Vaccined.choices, default=Vaccined.FULL
    )
    is_boostered = models.CharField(
        max_length=50, choices=Boostered.choices, default=Boostered.NEVER
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Assessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment_number = models.CharField(max_length=50, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    symptoms = models.CharField(max_length=1000, null=True)
    diagnosis = models.CharField(max_length=500, null=True)
    note = models.CharField(max_length=1000, null=True)
    
    def __str__(self):
        return self.assessment_number
    