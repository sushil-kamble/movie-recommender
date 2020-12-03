from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Review(models.Model):
    movie = models.CharField(max_length=80, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    review_description = models.TextField(default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.author.username

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.timestamp = timezone.now()
        self.timestamp = timezone.now()
        return super(Review, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})


class Watchlist(models.Model):
    movie = models.CharField(max_length=80, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie + " - " + self.author.username



