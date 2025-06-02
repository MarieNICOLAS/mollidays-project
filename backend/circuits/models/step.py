from django.db import models
from .circuit import Circuit


class Step(models.Model):
    circuit = models.ForeignKey(
        Circuit,
        on_delete=models.CASCADE,
        related_name="steps"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(help_text="Ordre de l'étape dans le circuit")
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = ('circuit', 'order')

    def __str__(self):
        return f"{self.title} (Étape {self.order})"
