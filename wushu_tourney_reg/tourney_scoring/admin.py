from django.contrib import admin
from .models import FinalScore, JudgeScore

# Register your models here.
class FinalScoreAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['registration', 'head_judge', 'final_score', 'final_rank']}),
    ]

    list_display = ['registration', 'head_judge', 'final_score', 'final_rank']
    list_filter = ['registration', 'head_judge','final_score', 'final_rank']
    search_fields = ['registration__registrant__users__first_name', 'registration__registrant__users__last_name', 
                     'registration__tournament_event__event__english_name',
                     'registration__tournament_event__tournament__name',
                     'final_score', 'final_rank']

class JudgeScoreAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['final_score', 'judge', 'judge_score', 'justification']}),
    ]

    list_display = ['final_score', 'judge', 'judge_score']
    list_filter = ['final_score', 'judge']
    search_fields = ['judge__first_name', 'judge__last_name', 'judge_score']

admin.site.register(FinalScore, FinalScoreAdmin)
admin.site.register(JudgeScore, JudgeScoreAdmin)