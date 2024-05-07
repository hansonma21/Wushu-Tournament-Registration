from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    """A user's profile; is a User; is a Registrant (for multiple tournaments); has Registrations (for multiple events); judges multiple TournamentEvents"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.TextField() # e.g. John
    last_name = models.TextField() # e.g. Doe
    birth_date = models.DateField() # e.g. 2000-01-01
    sex = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', "Female"),
    ])
    skill_level = models.TextField() # e.g. Beginner, Intermediate, Advanced

    email = models.EmailField() # e.g. example@gmail.com
    phone_number = models.TextField(null=True) # e.g. 123-456-7890 (null because optional)

    school_or_club = models.TextField(null=True) # e.g. Ohio Wushu Academy (null because optional)
    usawkf_id = models.TextField(null=True) # e.g. 123456 (null because optional)

class Tournament(models.Model):
    """A tournament that is being held (e.g. each annual tournament would be its own); has TournamentEvents; has Registrants"""

    name = models.TextField() # e.g. 6th Ohio International Chinese Martial Arts Tournament Registration 2024

    start_date = models.DateField() # e.g. 2024-08-03
    start_time = models.TimeField() # e.g. 09:00:00
    end_date = models.DateField() # e.g. 2024-08-03
    end_time = models.TimeField(null=True) # e.g. 18:00:00 (null if no end time)
    location = models.TextField() # e.g. Mintonette Sports

    registration_open = models.BooleanField() # e.g. True
    registration_start_date_time = models.DateTimeField() # e.g. 2024-05-01 00:00:00
    early_registration_end_date_time = models.DateTimeField(null=True) # e.g. 2024-06-01 23:59:59 (null if no early registration)
    registration_end_date_time = models.DateTimeField() # e.g. 2024-07-01 23:59:59

class Event(models.Model):
    """An event that can be part of a tournament (e.g. Taiji, Changquan, etc.); has TournamentEvents (defines the type of event the TournamentEvent is)"""

    english_name = models.TextField() # e.g. Compulsory Southern Fist
    chinese_name = models.TextField() # e.g. 规定南拳
    description = models.TextField(null=True) # e.g. Southern Fist is... (null if no description)
    rules = models.TextField(null=True) # e.g. Additional specifications/rules for this event

    min_age = models.IntegerField(null=True) # e.g. 18 (null if no minimum age)
    max_age = models.IntegerField(null=True) # e.g. 99 (null if no maximum age)

    skill_level = models.TextField() # e.g. Beginner, Intermediate, Advanced
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    type_of_form = models.TextField() # e.g. Traditional Barehand Form, Traditional Short Weapon, etc. (a classification of the type of form)
    is_group_event = models.BooleanField() # e.g. True (True if group, False if individual)
    is_weapon_event = models.BooleanField() # e.g. True (True if weapon, False if barehand)

class TournamentEvent(models.Model):
    """A specific event that is part of a tournament (e.g. 6th Ohio International Chinese Martial Arts Tournament Registration 2024 - Compulsory Southern Fist); has Registrations; belongs to a Tournament and an Event"""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    judges = models.ManyToManyField(Profile) # could be a list of judges for this event

    order = models.IntegerField() # e.g. 1 (the order in which the event is held in the tournament)
    mat_or_location = models.TextField() # e.g. Mat 1, Mat 2, etc.
    max_participants = models.IntegerField() # e.g. 50
    registration_open = models.BooleanField() # e.g. True, times are based on the tournament's registration_open, early_registration_end_date_time, and registration_end_date_time

class Registrant(models.Model):
    """A person/group who is registering for a specific tournament event; has Registrations, belongs to a Tournament, made up of User(s); has Registrations"""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    users = models.ManyToManyField(Profile) # could be a list of users for this registrant (e.g. a group)

    is_group = models.BooleanField() # e.g. True (True if group, False if individual)
    group_name = models.TextField(null=True) # e.g. John Doe (null if individual)
    first_name = models.TextField(null=True) # e.g. John (null if group)
    last_name = models.TextField(null=True) # e.g. Doe (null if group)
    school_or_club = models.TextField(null=True) # e.g. Ohio Wushu Academy

class Registration(models.Model):
    """A registration for a specific tournament event; has a singular Registrant; belongs to a TournamentEvent; has a Scoring (see tourney_scoring app); makes scoring Justifications (see tourney_scoring app)"""
    tournament_event = models.ForeignKey(TournamentEvent, on_delete=models.CASCADE)
    registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE) # could be a group or individual

    first_name = models.TextField() # e.g. John
    last_name = models.TextField() # e.g. Doe
    birth_date = models.DateField() # e.g. 2000-01-01
    email = models.EmailField() # e.g.

