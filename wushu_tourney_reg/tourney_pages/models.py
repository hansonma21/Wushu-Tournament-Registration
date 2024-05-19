from django.db import models

# Create your models here.
# add a news model to store news/updates articles
class News(models.Model):
    """A model to store news/updates articles"""
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.title