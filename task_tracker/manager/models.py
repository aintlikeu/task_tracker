from django.db import models
from accounts.models import CustomUser


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE,
                              related_name='owned_tasks',
                              to_field='username')
    assigned_to = models.ForeignKey(CustomUser,
                                    on_delete=models.CASCADE,
                                    related_name='assigned_tasks',
                                    blank=True, null=True,
                                    to_field='username')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} (by {self.owner}, assigned to {self.assigned_to})'
