from django.contrib import admin
from .models import FinalScore, JudgeScore

# Register your models here.
class FinalScoreAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['registration', 'final_score', 'final_rank']}),
    ]

    list_display = ['registration', 'final_score', 'final_rank']
    list_filter = ['registration', 'final_score', 'final_rank']
    search_fields = ['registration', 'final_score', 'final_rank']

class JudgeScoreAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['final_score', 'judge', 'judge_score', 'justification']}),
    ]

    list_display = ['final_score', 'judge', 'judge_score']
    list_filter = ['final_score', 'judge']
    search_fields = ['final_score', 'judge', 'judge_score']

admin.site.register(FinalScore, FinalScoreAdmin)
admin.site.register(JudgeScore, JudgeScoreAdmin)