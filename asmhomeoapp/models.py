from django.db import models


class Visit(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Visit Count: {self.count}"

