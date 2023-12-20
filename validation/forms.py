# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Participant, Car
from django.utils import timezone


def validate_age(value):
    today = timezone.now().date()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Participants must be 18 years or older.")
    
    


class ParticipantForm(forms.ModelForm):
    class Meta:
        model =Participant
        fields = ['firstname', 'middlename', 'lastname', 'email', 'ref_number', 'gender', 'date_of_birth','telephone']
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]


    firstname = forms.CharField(
        max_length=255,
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    middlename = forms.CharField(
        max_length=255,
        required=False,
        label='Middle Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    lastname = forms.CharField(
        max_length=255,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    ref_number = forms.IntegerField(
       
        label='Reference Number',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='Gender',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'class': 'form-control datepicker','type': 'date','data-date-format':'DD MMMM YYYY','data-date':''}),
        validators=[validate_age]
    )
    telephone = forms.CharField(
        label='Telephone', 
        max_length=15,  
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Tel +250'})
        )
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not str(telephone).startswith('+250'):
            raise forms.ValidationError("Telephone number must start with +250.")
        return telephone

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['plate_type', 'make', 'model', 'color', 'plate_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Add Bootstrap classes or any other customization for specific fields if needed
        self.fields['plate_type'].widget.attrs['class'] = 'form-select'  # Bootstrap class for select input

    def clean_plate_number(self):
        plate_type = self.cleaned_data.get('plate_type')
        plate_number = self.cleaned_data.get('plate_number').upper()  # Convert to uppercase for case-insensitive comparison

        if plate_type == Car.PERSONAL_CAR:
            if not plate_number.startswith('RA') or len(plate_number) != 7 or not plate_number[3:6].isdigit():
                raise forms.ValidationError('Invalid Personal Car plate format.')

        elif plate_type in Car.SECURITY_ORGANS_CAR:
            valid_prefixes = Car.SECURITY_ORGANS_CAR
            if not any(plate_number.startswith(prefix) for prefix in valid_prefixes) or len(plate_number) != 7 or not plate_number[3:6].isdigit():
                raise forms.ValidationError('Invalid Security Organs Car plate format.')

        elif plate_type in Car.GOVERNMENT_MANAGED:
            valid_prefixes = Car.GOVERNMENT_MANAGED
            if not any(plate_number.startswith(prefix) for prefix in valid_prefixes) or len(plate_number) != 6 or not plate_number[2:5].isdigit():
                raise forms.ValidationError('Invalid Government Managed plate format.')

        return plate_number