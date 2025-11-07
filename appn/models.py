from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
import random
from django.conf import settings

# User Roles
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('organizer', 'Organizer'),
    ('participant', 'Participant'),
)

STATUS_CHOICES = (
    ('Upcoming', 'Upcoming'),
    ('Ongoing', 'Ongoing'),
    ('Completed', 'Completed')
)

CATEGORY_CHOICES = (
    ('Sports', 'Sports'),
    ('Cultural', 'Cultural'),
    ('Technical', 'Technical'),
    ('Other', 'Other'),
)

class CustomUser(AbstractUser):
    # New Fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()

    role = models.CharField(
        max_length=11,  # Increased length to match the longest choice ('participant')
        choices=ROLE_CHOICES,
        default='participant'
    )
    unique_id = models.CharField(max_length=5, unique=True, editable=False)

    # Adding related_name to avoid reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Avoids clash with auth.User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Avoids clash with auth.User.user_permissions
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            unique_id = str(random.randint(10000, 99999))
            if not CustomUser.objects.filter(unique_id=unique_id).exists():
                return unique_id


class Event(models.Model):
    # Fields as per your requirements
    eid = models.CharField(max_length=5, unique=True, editable=False)  # 5-digit unique EID
    name = models.CharField(max_length=100)
    organiser = models.CharField(max_length=100)
    sponsor = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    event_datetime = models.DateTimeField()  # Calendar & watch widget
    one_line_description = models.CharField(max_length=255)
    complete_description = models.TextField()
    eligibility = models.TextField()
    rewards = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Upcoming')
    winner = models.CharField(max_length=100, null=True, blank=True)  # Only for Completed events

    def save(self, *args, **kwargs):
        # Generate a unique 5-digit EID if not already assigned
        if not self.eid:
            self.eid = self.generate_unique_eid()
        super().save(*args, **kwargs)

    def generate_unique_eid(self):
        while True:
            eid = str(random.randint(10000, 99999))
            if not Event.objects.filter(eid=eid).exists():
                return eid

    def __str__(self):
        return f"{self.name} ({self.eid})"
    

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use AUTH_USER_MODEL to refer to the custom user model
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )

    def __str__(self):
        return f"{self.full_name} - {self.event.name}"

