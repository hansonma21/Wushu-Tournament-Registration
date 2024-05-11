from django.contrib import admin
from .models import AgeGroup, Profile, Tournament, Event, TournamentEvent, Registration, Registrant
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class TournamentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General Information', {'fields': ['name', 'start_date_time', 'end_date_time', 'location']}),
        ('Registration', {'fields': ['registration_start_date_time', 
                                     'early_registration_end_date_time', 
                                     'registration_end_date_time']}),
        ('Status', {'fields': ['registration_open', 'is_active', 'is_locked']}),
    ]

    list_display = ['name', 'start_date_time', 'registration_open', 'location', 'is_active', 'is_locked']
    list_filter = ['start_date_time', 'location', 'is_active', 'is_locked']
    search_fields = ['name', 'location']

class AgeGroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['min_age', 'max_age']}),
    ]

    list_display = ['min_age', 'max_age']
    list_filter = ['min_age', 'max_age']
    search_fields = ['min_age', 'max_age']

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['english_name', 'chinese_name', 
                           'age_group', 'skill_level', 
                           'sex', 'type_of_form']}),
        ('Classifications', {'fields': ['is_group_event', 'is_weapon_event', 
                                        'is_taolu_event', 'is_nandu_event']}),
        ('Additional Information', {
            'classes': ['collapse'], # 'collapse' hides the fieldset by default
            'fields': ['description', 'judging_criteria', 'rules']})
    ]

    list_display = ['english_name', 'chinese_name', 'age_group', 'skill_level', 'sex', 'type_of_form']
    list_filter = ['age_group', 'skill_level', 'sex', 'type_of_form']
    search_fields = ['english_name', 'chinese_name']

    def age_group(self, obj):
        if obj.max_age is not None:
            return obj.min_age + '-' + obj.max_age
        else:
            return obj.min_age + '+'

class TournamentEventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['tournament', 'event', 'mat_or_location', 'order', 'judges']}),
        ('Status', {'fields': ['registration_open', 'is_active', 'is_locked']}),
    ]

    list_display = ['tournament', 'event', 'mat_or_location', 'registration_open', 'is_active', 'is_locked']
    list_filter = ['tournament', 'event', 'mat_or_location', 'is_active', 'is_locked']
    search_fields = ['tournament', 'event', 'mat_or_location']
    filter_horizontal = ('judges',)

class RegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['registrant', 'tournament_event']}),
        ('Status', {'fields': ['is_paid', 'is_withdrawn', 'is_checked_in', 'is_disqualified', 'is_completed']}),
        ('Additional Information', {'fields': ['notes', 'registered_date_time']})
    ]

    list_display = ['tournament_event', 'registrant_name', 'registered_date_time', 'is_paid', 'is_withdrawn', 'is_checked_in', 'is_disqualified', 'is_completed']
    list_filter = ['tournament_event__tournament', 'tournament_event__event', 'is_paid', 'is_withdrawn', 'is_checked_in', 'is_disqualified', 'is_completed']
    search_fields = ['tournament_event__tournament', 'tournament_event__event', 'registrant__group_name', 'registrant__users__first_name', 'registrant__users__last_name', 'registrant__users__email']

    def registrant_name(self, obj):
        return obj.registrant.get_registrant_name()

class RegistrantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['group_name', 'users']}),
        ('Status', {'fields': ['is_active']}),
        ('Additional Information', {'fields': ['notes', 'created_date_time']})
    ]

    list_display = ['tournament', 'is_group', 'registrant_name', 'school_or_club', 'is_kungfu_team_competitor']
    list_filter = ['tournament', 'is_group', 'is_kungfu_team_competitor', 'school_or_club']
    search_fields = ['group_name', 'users__first_name', 'users__last_name', 'users__email']

    def registrant_name(self, obj):
        return obj.get_registrant_name()

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(AgeGroup, AgeGroupAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(TournamentEvent, TournamentEventAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Registrant, RegistrantAdmin)