from django.db import models

class Feedback(models.Model):
    CROWDED_CHOICES = [
        ('uncrowded', 'Uncrowded'),
        ('less_crowded', 'Less Crowded'),
        ('relatively_crowded', 'Relatively Crowded'),
        ('crowded', 'Crowded'),
    ]


    name = models.CharField(max_length=100)
    crowded_level = models.CharField(max_length=20, choices=CROWDED_CHOICES, default='uncrowded')
    message = models.TextField()
    station_name = models.CharField(max_length=255, default='Unknown Station')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.station_name}"
