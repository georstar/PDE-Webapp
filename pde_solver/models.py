from django.db import models


class PDESolution(models.Model):
    """Model to store PDE solutions"""
    equation = models.TextField(help_text="The partial differential equation")
    boundary_conditions = models.TextField(blank=True, help_text="Boundary conditions")
    initial_conditions = models.TextField(blank=True, help_text="Initial conditions")
    solution = models.TextField(help_text="The solution to the PDE")
    method_used = models.CharField(max_length=100, help_text="Method used to solve")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "PDE Solution"
        verbose_name_plural = "PDE Solutions"

    def __str__(self):
        return f"PDE: {self.equation[:50]}... ({self.created_at.strftime('%Y-%m-%d')})"
