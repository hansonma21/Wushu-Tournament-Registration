from django.forms import ModelForm
from .models import FinalScore, JudgeScore

class FinalScoreForm(ModelForm):
    class Meta:
        model = FinalScore
        fields = ['final_score', 'final_rank']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['final_score'].widget.attrs.update({'placeholder': '0.0 - 10.0'})
        self.fields['final_rank'].widget.attrs.update({'placeholder': 'e.g. 1 - 10'})

        self.fields['final_score'].widget.attrs.update({'class': 'form-control border border-gray-300'})
        self.fields['final_rank'].widget.attrs.update({'class': 'form-control border border-gray-300'})


class JudgeScoreForm(ModelForm):
    class Meta:
        model = JudgeScore
        fields = ['judge_score', 'justification']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['judge_score'].widget.attrs.update({'placeholder': '0.0 - 10.0'})
        self.fields['justification'].widget.attrs.update({'placeholder': 'e.g. The competitor lost balance during the form'})

        self.fields['judge_score'].widget.attrs.update({'class': 'form-control border border-gray-300'})
        self.fields['justification'].widget.attrs.update({'class': 'form-control border border-gray-300'})