from django.shortcuts import render
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .forms import ParticipantForm,CarForm
from .models import Car, Participant


def success_page(request):
    return render(request, 'Success/Success.html')


# Register User View

def signup(request):
    
    return render(request,'Users/SignUp.html')

# Hmoe View

def home(request):
    
    return render(request,'Success/Home.html')

def register_participant(request):
    CarFormSet = inlineformset_factory(Participant, Car, form=CarForm, extra=1, can_delete=True)

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        car_formset = CarFormSet(request.POST, instance=Participant())

        if participant_form.is_valid() and car_formset.is_valid():
            participant = participant_form.save()

            # Set the plate type for each car in the formset
            for car_form in car_formset:
                car = car_form.save(commit=False)
                car.participant = participant
                car.save()

                return redirect('success_page')

    else:
        participant_form = ParticipantForm()
        car_formset = CarFormSet(instance=Participant())

    return render(request, 'Validation/Register.html', {'participant_form': participant_form, 'car_formset': car_formset})

def add_car(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    CarFormSet = inlineformset_factory(Participant, Car, form=CarForm, extra=1, can_delete=True)

    if request.method == 'POST':
        car_formset = CarFormSet(request.POST, instance=participant)

        if car_formset.is_valid():
            car_formset.save()

    return redirect('success_page')