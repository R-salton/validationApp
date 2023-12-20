from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField

def validate_age(value):
    today = timezone.now().date()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Participants must be 18 years or older.")

class Participant(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    firstname = models.CharField(max_length=255, verbose_name='First Name')
    middlename = models.CharField(max_length=255, blank=True, null=True, verbose_name='Middle Name')
    lastname = models.CharField(max_length=255, verbose_name='Last Name')
    email = models.EmailField(unique=True, verbose_name='Email')
    ref_number = models.IntegerField(validators=[MinValueValidator(99), MaxValueValidator(999)],verbose_name='Reference Number')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Gender')
    date_of_birth = models.DateField(validators=[validate_age], verbose_name='Date of Birth')
    telephone: PhoneNumberField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"



class Car(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default='')
    PERSONAL_CAR = 'RA'
    SECURITY_ORGANS_CAR = ['RDF', 'RNP']
    GOVERNMENT_MANAGED = ['GP', 'GR', 'IT']

    PLATE_TYPE_CHOICES = [
        (PERSONAL_CAR, 'Personal Car Plate'),
        (SECURITY_ORGANS_CAR[0], 'Security Organs Car Plate (RDF)'),
        (SECURITY_ORGANS_CAR[1], 'Security Organs Car Plate (RNP)'),
        (GOVERNMENT_MANAGED[0], 'Government Managed Plate (GP)'),
        (GOVERNMENT_MANAGED[1], 'Government Managed Plate (GR)'),
        (GOVERNMENT_MANAGED[2], 'Government Managed Plate (IT)'),
    ]

    plate_type = models.CharField(max_length=3, choices=PLATE_TYPE_CHOICES)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=10)  # Adjust max_length as needed

    def clean_plate_number(self):
        plate_type = self.plate_type
        plate_number = self.plate_number.upper()  # Convert to uppercase for case-insensitive comparison

        if plate_type == self.PERSONAL_CAR:
            if not plate_number.startswith('RA') or len(plate_number) != 7 or not plate_number[3:6].isdigit():
                raise ValidationError('Invalid Personal Car plate format.')

        elif plate_type in self.SECURITY_ORGANS_CAR:
            if not (plate_number.startswith('RNP') or plate_number.startswith('RDF')) or len(plate_number) != 7 or not plate_number[3:6].isdigit():
                raise ValidationError('Invalid Security Organs Car plate format.')

        elif plate_type in self.GOVERNMENT_MANAGED:
            valid_prefixes = self.GOVERNMENT_MANAGED
            if not any(plate_number.startswith(prefix) for prefix in valid_prefixes) or len(plate_number) != 6 or not plate_number[2:5].isdigit():
                raise ValidationError('Invalid Government Managed plate format.')
