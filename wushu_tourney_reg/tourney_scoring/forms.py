from django.forms import ModelForm
from .models import FinalScore, JudgeScore

class FinalScoreForm(ModelForm):
    class Meta:
        model = FinalScore
        fields = ['final_score', 'final_rank']

class JudgeScoreForm(ModelForm):
    class Meta:
        model = JudgeScore
        fields = ['judge_score', 'justification']