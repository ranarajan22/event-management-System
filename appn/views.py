from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, EventForm, RegistrationForm
from .models import Event, Registration
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


def is_organiser_or_admin(user):
    return user.role in ['organiser', 'admin']

def is_admin(user):
    return user.role in ['admin']

def is_participant(user):
    return user.role in ['participant']

@login_required
def index(request):
    return render(request, 'index.html')  

def events(request):
    events = Event.objects.all()  # Fetch all events, or modify as needed
    return render(request, 'events.html', {'events': events})  # Render to the 'events.html' template

def land(request):
    return render(request, 'land.html')  # or any other template you need


@login_required
def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Logged in as {user.username}.")
            
            # Redirect based on user role
            if user.role == 'participant':
                return redirect('index')  # Redirect to index.html for participants
            elif user.role in ['organiser', 'admin']:
                return redirect('home')  # Redirect to home.html for organizers/admins
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, f"Logged in as {user.username}.")
#             return redirect('index')
#         else:
#             messages.error(request, "Invalid username or password.")
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('land')

@login_required
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html', {'user': request.user})

# List all events
@login_required
def event_list(request):
    events = Event.objects.all()

    # Annotate each event with a flag indicating if the user is registered
    for event in events:
        event.is_registered = event.registrations.filter(user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'event_list.html', {'events': events})

# View to display the event details
@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

# Create a new event
@login_required
@user_passes_test(is_organiser_or_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

# Update an existing event
@login_required
@user_passes_test(is_organiser_or_admin)
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

# Delete an event
@login_required
@user_passes_test(is_admin)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})

@login_required
@user_passes_test(is_participant)
def event_register(request, event_id):
    event = get_object_or_404(Event, pk=event_id, status='Upcoming')
    existing_registration = Registration.objects.filter(event=event, user=request.user).first()

    if existing_registration:
        messages.info(request, "You have already registered for this event.")
        return redirect('event_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            messages.success(request, "Successfully registered for the event!")
            return redirect('event_list')
    else:
        form = RegistrationForm()

    return render(request, 'event_register.html', {'form': form, 'event': event})

@login_required
@user_passes_test(is_organiser_or_admin)
def event_registrations(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user.role not in ['admin', 'organizer']:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('event_list')

    registrations = event.registrations.all()
    return render(request, 'event_registrations.html', {'event': event, 'registrations': registrations})


