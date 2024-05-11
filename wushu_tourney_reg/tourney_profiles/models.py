from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sexes(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'

class SkillLevels(models.TextChoices):
    BEGINNER = 'beginner', 'Beginner'
    INTERMEDIATE = 'intermediate', 'Intermediate'
    ADVANCED = 'advanced', 'Advanced'


class Profile(models.Model):
    """A user's profile; is a User; is a Registrant (for multiple tournaments); has Registrations (for multiple events); can judge multiple TournamentEvents"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True) # e.g. profile picture (null because optional)

    first_name = models.TextField() # e.g. John
    middle_name = models.TextField(null=True, blank=True) # e.g. Quincy (null because optional)
    last_name = models.TextField() # e.g. Doe
    birth_date = models.DateField() # e.g. 2000-01-01
    sex = models.CharField(max_length=20, choices=Sexes.choices)
    skill_level = models.TextField(null=True, choices=SkillLevels.choices) # e.g. Beginner, Intermediate, Advanced (not decided yet, null because optional)

    email = models.EmailField() # e.g. example@gmail.com, REQUIRED
    phone_number = models.TextField(null=True, blank=True) # e.g. 123-456-7890 (null because optional)

    school_or_club = models.TextField(null=True, blank=True) # e.g. Ohio Wushu Academy (null because optional)

    usawkf_id = models.TextField(blank=True, null=True, unique=True) # e.g. 123456 (null because optional)

    is_judge = models.BooleanField(default=False) # e.g. True (True if judge, False if not)

    class Meta:
        ordering = ['last_name', 'first_name']

        # Ensure that the email and usawkf_id are unique
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email', violation_error_message='This email is already in use.'),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username}, {self.email})"