from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, Count

from .models import Event, Registration
from .forms import EventForm, RegistrationForm


@login_required
def home(request):
    return render(request, 'events/home.html')

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_new.html', {'form': form})

@login_required
def event_list(request):
    query = request.GET.get('q')
    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(date__icontains=query)
        ).annotate(num_registrations=Count('registration'))
    else:
        #events = Event.objects.all()
        events = Event.objects.all().annotate(num_registrations=Count('registration'))
    return render(request, 'events/event_list.html', {'events': events})

#def event_list(request):
#    events = Event.objects.annotate(num_registrations=Count('registration'))
#    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event)
    
    user_is_registered = False
    if request.user.is_authenticated:
        user_is_registered = Registration.objects.filter(event=event, user=request.user).exists()
        
        context = {
            'event': event, 
            'registrations': registrations,
            'user_is_registered': user_is_registered,
        }
    return render(request, 'events/event_detail.html', context=context)

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    user_is_registered = False
    if request.user.is_authenticated:
        user_is_registered = Registration.objects.filter(event=event, user=request.user).exists()
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            send_mail(
                'Confirmation d\'inscription',
                f'Vous êtes inscrit à l\'événement : {event.title}',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
            )
            return redirect('event_detail', event_id=event.id)
    else:
        form = RegistrationForm()
        
    return render(request, 'events/register_event.html', {'form': form, 'event': event, 'user_is_registered': user_is_registered})
