from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):

    class Meta:
        model = Reporte

        # codigo, fecha_creacion y fecha_actualizacion NO van: son automáticos
        fields = [
            'tipo', 'area', 'responsable', 'periodo',
            'fecha_inicio', 'fecha_fin', 'estado'
        ]

        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'periodo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Julio 2026'
            }),

            'fecha_inicio': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),

            'fecha_fin': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),

            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('fecha_inicio')
        fin = cleaned.get('fecha_fin')

        # Regla de negocio: el periodo no puede terminar antes de empezar
        if inicio and fin and fin < inicio:
            raise forms.ValidationError(
                'La fecha de fin no puede ser anterior a la fecha de inicio.'
            )

        return cleaned