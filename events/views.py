from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, EventRegistration
from .forms import EventForm, EventRegistrationForm


def event_list(request):
    events = Event.objects.filter(visibility='public').order_by('date_time')
    return render(request, 'events/list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration_form = None

    if event.event_type == 'registration_required':
        if request.method == 'POST':
            registration_form = EventRegistrationForm(request.POST)
            if registration_form.is_valid():
                registration = registration_form.save(commit=False)
                registration.event = event
                registration.save()
                messages.success(request, "You have successfully registered.")
                return redirect('event_detail', event_id=event.id)
        else:
            registration_form = EventRegistrationForm()

    context = {
        'event': event,
        'registration_form': registration_form
    }
    return render(request, 'events/detail.html', context)


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('clubs:club_profile_events')
    else:
        form = EventForm()
    return render(request, 'events/registation.html', {'form': form})
