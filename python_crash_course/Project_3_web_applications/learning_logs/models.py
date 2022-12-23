from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    """Create a foreign key to access the each particular topic"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        # INFO: Django calls a __str__ method to display a simple representation of a model
        return self.text


class Entry(models.Model):
    """Something specific learned about a topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"  # INFO: Meta Class holds extra information for managing a model.

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.text[:50]}..." if len(self.text) > 50 else f"{self.text}"
