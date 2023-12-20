# admin.py
from django.contrib import admin
from .models import Participant, Car

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'email', 'ref_number', 'gender', 'date_of_birth']
    search_fields = ['firstname', 'lastname', 'email']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'color', 'plate_type', 'plate_number']
    search_fields = ['make', 'model', 'plate_number', 'plate_type']
