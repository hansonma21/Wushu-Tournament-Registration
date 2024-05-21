from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from tourney_profiles.models import Profile, SkillLevels, Sexes

class AgeGroup(models.Model):
    """An age group for an event; has a minimum and maximum age; part of Events"""
    min_age = models.IntegerField(validators=[MinValueValidator(0)]) # e.g. 18
    max_age = models.IntegerField(null=True, blank=True) # e.g. 99 (null if no maximum age like 60+)
    is_active = models.BooleanField(default=True) # e.g. True

    class Meta:
        ordering = ['min_age', 'max_age']

        # Ensure that the min_age is non-negative
        constraints = [
            models.UniqueConstraint(fields=['min_age', 'max_age'], name='unique_age_group', violation_error_message='This age group already exists.'),
            models.CheckConstraint(check=models.Q(min_age__lte=models.F('max_age')), name='min_age_before_max_age', violation_error_message='The minimum age must be the same as or before the maximum age.'),
            models.CheckConstraint(check=models.Q(min_age__gte=0), name='min_age_non_negative', violation_error_message='The minimum age must be non-negative.')
        ]

    def __str__(self):
        if self.max_age is not None:
            return f"{self.min_age}-{self.max_age}"
        else:
            return f"{self.min_age}+"

class Tournament(models.Model):
    """A tournament that is being held (e.g. each annual tournament would be its own); has TournamentEvents; has Registrants"""

    name = models.TextField() # e.g. 6th Ohio International Chinese Martial Arts Tournament Registration 2024

    start_date_time = models.DateTimeField() # e.g. 2024-08-01 00:00:00
    end_date_time = models.DateTimeField() # e.g. 2024-08-01 23:59:59
    location = models.TextField() # e.g. Mintonette Sports

    registration_open = models.BooleanField() # e.g. True
    registration_start_date_time = models.DateTimeField() # e.g. 2024-05-01 00:00:00
    early_registration_end_date_time = models.DateTimeField(blank=True, null=True) # e.g. 2024-06-01 23:59:59 (null if no early registration)
    registration_end_date_time = models.DateTimeField() # e.g. 2024-07-01 23:59:59

    is_active = models.BooleanField(default=True) # e.g. True
    is_locked = models.BooleanField(default=False) # e.g. False

    class Meta:
        ordering = ['start_date_time']

        # Ensure that the name, start_date, and location are unique, 
        # that the start_date is the day of or before the end_date, 
        # and that the registration_start_date_time is before the registration_end_date_time, 
        # and that the early_registration_end_date_time is before the registration_end_date_time (if it exists)
        # and that the registration_start_date_time is before the early_registration_end_date_time (if it exists)
        constraints = [
            models.UniqueConstraint(fields=['name', 'start_date_time', 'location'], name='unique_tournament', violation_error_message='This tournament already exists.'),
            models.CheckConstraint(check=models.Q(start_date_time__lte=models.F('end_date_time')), name='start_date_before_end_date',
                violation_error_message='The start date must be the same day as or before the end date.'),
            models.CheckConstraint(check=models.Q(registration_start_date_time__lte=models.F('registration_end_date_time')), name='registration_start_date_time_before_registration_end_date_time',
                violation_error_message='The registration start date time must be before the registration end date time.'),
            models.CheckConstraint(check=models.Q(early_registration_end_date_time__isnull=True) | models.Q(registration_start_date_time__lte=models.F('early_registration_end_date_time')), 
                                   name='registration_start_date_time_before_early_registration_end_date_time_or_null',
                                   violation_error_message='The registration start date time must be before the early registration end date time or the early registration end date time must be null'),
            models.CheckConstraint(check=models.Q(early_registration_end_date_time__isnull=True) | models.Q(early_registration_end_date_time__lte=models.F('registration_end_date_time')), 
                                   name='early_registration_end_date_time_before_registration_end_date_time_or_null',
                                   violation_error_message='The early registration end date time must be before the registration end date time or null.'),
        ]

    def __str__(self):
        return f"{self.name} ({self.start_date_time.year})"

class Event(models.Model):
    """An event that can be part of a tournament (e.g. Taiji, Changquan, etc.); has TournamentEvents (defines the type of event the TournamentEvent is); has an AgeGroup"""
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    english_name = models.TextField() # e.g. Compulsory Southern Fist
    chinese_name = models.TextField() # e.g. 规定南拳
    description = models.TextField(null=True, blank=True) # e.g. Southern Fist is... (null if no description)
    judging_criteria = models.TextField(null=True, blank=True) # e.g. Judging criteria for this event (null if no judging criteria)
    rules = models.TextField(null=True, blank=True) # e.g. Additional specifications/rules for this event

    skill_level = models.TextField(choices=SkillLevels.choices) # e.g. Beginner, Intermediate, Advanced
    sex = models.CharField(max_length=20, choices=Sexes.choices)
    type_of_form = models.TextField() # e.g. Traditional Barehand Form, Traditional Short Weapon, etc. (a classification of the type of form)
    is_group_event = models.BooleanField() # e.g. True (True if group, False if individual)
    is_weapon_event = models.BooleanField() # e.g. True (True if weapon, False if barehand)
    is_taolu_event = models.BooleanField() # e.g. True (True if taolu, False if sanda)
    is_nandu_event = models.BooleanField() # e.g. True (True if nandu, False if not)

    class Meta:
        ordering = ['english_name', 'sex', 'skill_level']

        # Ensure that the english_name, chinese_name, skill_level, age_group, sex are unique,
        constraints = [
            models.UniqueConstraint(fields=['english_name', 'chinese_name', 'skill_level', 'age_group', 'sex'], name='unique_event', violation_error_message='This event already exists.'),
        ]
    
    def __str__(self):
        return f"{self.english_name} ({self.chinese_name}), {self.skill_level}, {self.age_group}, {self.skill_level}, {self.sex}"


class TournamentEvent(models.Model):
    """A specific event that is part of a tournament (e.g. 6th Ohio International Chinese Martial Arts Tournament Registration 2024 - Compulsory Southern Fist); has Registrations; belongs to a Tournament and an Event"""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    judges = models.ManyToManyField(Profile, limit_choices_to={'is_judge': True}, blank=True) # could be a list of judges for this event
    # can access registrations for this tournament event by accessing the Registrations that have this tournament_event

    order = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True) # e.g. 1 (the order in which the event is held in the tournament)
    mat_or_location = models.TextField() # e.g. Mat 1, Mat 2, etc.
    max_participants = models.IntegerField(validators=[MinValueValidator(1)], default=999) # e.g. 50

    registration_open = models.BooleanField() # e.g. True, times are based on the tournament's registration_open, early_registration_end_date_time, and registration_end_date_time
    is_active = models.BooleanField(default=True) # e.g. True
    is_locked = models.BooleanField(default=False) # e.g. False

    class Meta:
        ordering = ['tournament', 'mat_or_location', 'event', 'order']

        # Ensure that the order is non-negative and greater than or equal to 1,
        # that the max_participants is non-negative and greater than or equal to 1,
        # that the order is unique for the tournament and mat_or_location,
        # that the tournament and event are unique
        constraints = [
            models.CheckConstraint(check=models.Q(order__gte=1), name='order_non_negative', violation_error_message='The order must be non-negative.'),
            models.CheckConstraint(check=models.Q(max_participants__gte=1), name='max_participants_non_negative', violation_error_message='The maximum number of participants must be non-negative.'),
            models.UniqueConstraint(fields=['tournament', 'order', 'mat_or_location'], name='unique_tournament_event_order', violation_error_message='This order already exists.'),
            models.UniqueConstraint(fields=['tournament', 'event'], name='unique_tournament_event', violation_error_message='This event already exists.')
        ]

    def __str__(self):
        return f"{self.tournament.name} - {self.event.english_name} - {self.mat_or_location} - #{self.order}"

class Registrant(models.Model):
    """A person/group who is registering for tournament events; has Registrations, belongs to a Tournament, made up of User(s); has Registrations"""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    users = models.ManyToManyField(Profile) # could be a list of users for this registrant (e.g. a group)

    created_date_time = models.DateTimeField(default=timezone.now) # e.g. 2024-07-01 12:00:00
    is_group = models.BooleanField() # e.g. True (True if group, False if individual)
    group_name = models.TextField(blank=True, null=True) # e.g. John Doe (null if individual)

    school_or_club = models.TextField(blank=True, null=True) # e.g. Ohio Wushu Academy

    is_kungfu_team_competitor = models.BooleanField() # e.g. True (True if kungfu team competitor, False if not)

    class Meta:
        ordering = ['tournament', 'group_name', 'users__first_name', 'users__last_name']

        # Ensure that the group_name is unique for the tournament if it is a group,
        # that the group_name is not null if it is a group,
        # that the group_name is null if it is not a group,
        # if is not group, then only one user can be in the registrant
        constraints = [
            models.UniqueConstraint(fields=['tournament', 'group_name'], name='unique_group_name', violation_error_message='This group name already exists.'),
            models.CheckConstraint(check=models.Q(group_name__isnull=False) | models.Q(is_group=False), name='group_name_not_null_if_group', violation_error_message='The group name must not be null if it is a group.'),
            models.CheckConstraint(check=models.Q(group_name__isnull=True) | models.Q(is_group=True), name='group_name_null_if_not_group', violation_error_message='The group name must be null if it is not a group.'),
        ]
    
    def __str__(self):
        if self.is_group:
            return f"{self.tournament.name} ({self.group_name})"
        else:
            return f"{self.users.first()}"
    
    def get_registrant_name(self):
        if self.is_group:
            return self.group_name
        else:
            return f"{self.users.first().first_name} {self.users.first().last_name}"
    
    def get_registrant_first_name(self):
        if self.is_group:
            raise ValidationError("This is a group registrant.")
        else:
            return self.users.first().first_name
    
    def get_registrant_last_name(self):
        if self.is_group:
            raise ValidationError("This is a group registrant.")
        else:
            return self.users.first().last_name
    
    def get_registrant_group_name(self):
        if self.is_group:
            return self.group_name
        else:
            raise ValidationError("This is an individual registrant.")




class Registration(models.Model):
    """A registration for a specific tournament event; has a singular Registrant; belongs to a TournamentEvent; has a Scoring (see tourney_scoring app); makes scoring Justifications (see tourney_scoring app)"""
    tournament_event = models.ForeignKey(TournamentEvent, on_delete=models.CASCADE)
    registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE) # could be a group or individual

    order = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True) # e.g. 1 (the order in which the registrant is registered in the tournament event)

    notes = models.TextField(null=True, blank=True) # e.g. Will pay at the door (null if no notes)
    registered_date_time = models.DateTimeField(default=timezone.now) # e.g. 2024-07-01 12:00:00

    is_paid = models.BooleanField() # e.g. True
    is_withdrawn = models.BooleanField(default=False) # e.g. False
    is_checked_in = models.BooleanField(default=False) # e.g. False
    is_disqualified = models.BooleanField(default=False) # e.g. False
    is_completed = models.BooleanField(default=False) # e.g. False

    class Meta:
        ordering = ['tournament_event', 'registrant']

        constraints = [
            models.UniqueConstraint(fields=['tournament_event', 'registrant'], name='unique_registration', violation_error_message='This registrant is already registered for this event.'),
            models.CheckConstraint(check=models.Q(order__gte=1), name='registration_order_non_negative', violation_error_message='The order must be non-negative.'),
            models.UniqueConstraint(fields=['tournament_event', 'order'], name='unique_registration_order', violation_error_message='This order already exists.'),
        ]
    
    def save(self, *args, **kwargs):
        if self.registered_date_time > timezone.now():
            raise ValidationError("The registration date time cannot be in the future.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.tournament_event} - {self.registrant}"



