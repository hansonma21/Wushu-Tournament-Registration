from django.db import models

from tourney_reg.models import Registration, Profile, TournamentEvent
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class FinalScore(models.Model):
    """A scoring for a registrant's performance in a tournament event; belongs to a singular Registration; has Justifications; has a Head Judge"""
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    head_judge = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='head_judge', null=True, blank=True, limit_choices_to={'is_judge': True}) # head judge dictates the final score and rank

    final_score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)]) # e.g. 9.5
    final_rank = models.IntegerField(null=True, blank=True) # e.g. 1, probably start off as null

    class Meta:
        ordering = ['registration', 'final_rank', 'final_score']

        constraints = [
            models.UniqueConstraint(fields=['registration', 'final_rank'], name='unique_registration_final_rank'),
            models.CheckConstraint(check=models.Q(final_score__gte=0) & models.Q(final_score__lte=10), name='final_score_range', violation_error_message='Score must be between 0 and 10'),
            models.CheckConstraint(check=models.Q(final_rank__gte=1), name='rank_range', violation_error_message='Rank must be greater than 1')
        ]

    def __str__(self):
        return f"{self.registration} - {self.final_score} - {self.final_rank}"

class JudgeScore(models.Model):
    """A justification for a scoring; belongs to a singular Scoring"""
    final_score = models.ForeignKey(FinalScore, on_delete=models.CASCADE)
    judge = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'is_judge': True})

    judge_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)]) # individual judge's score, e.g. 8.5
    justification = models.TextField(null=True, blank=True) # e.g. The competitor did not perform the required number of kicks

    class Meta:
        ordering = ['final_score', 'judge', 'judge_score']

        constraints = [
            models.UniqueConstraint(fields=['final_score', 'judge'], name='unique_judge_scoring'),
            models.CheckConstraint(check=models.Q(judge_score__gte=0) & models.Q(judge_score__lte=10), name='judge_score_range', violation_error_message='Score must be between 0 and 10')
        ]

    def __str__(self):
        return f"{self.final_score} - {self.judge} - {self.judge_score} - {self.justification}"