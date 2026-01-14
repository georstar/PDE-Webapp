from django import forms
from .models import PDESolution


class PDEInputForm(forms.ModelForm):
    """Form for inputting PDE and conditions"""
    
    class Meta:
        model = PDESolution
        fields = ['equation', 'boundary_conditions', 'initial_conditions']
        widgets = {
            'equation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., d²u/dt² = c²(d²u/dx²)\nOr: u_t = u_xx\nOr: d²u/dx² + d²u/dy² = 0',
                'required': True
            }),
            'boundary_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'e.g., u(0,t) = 0, u(L,t) = 0\nOr leave blank if not needed'
            }),
            'initial_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'e.g., u(x,0) = sin(x), u_t(x,0) = 0\nOr leave blank if not needed'
            }),
        }
        labels = {
            'equation': 'Partial Differential Equation',
            'boundary_conditions': 'Boundary Conditions (Optional)',
            'initial_conditions': 'Initial Conditions (Optional)',
        }
        help_texts = {
            'equation': 'Enter the PDE using standard mathematical notation',
            'boundary_conditions': 'Specify any boundary conditions for the domain',
            'initial_conditions': 'Specify any initial conditions',
        }
