from django import forms
from django.utils import timezone

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'priority']
        widgets = {
            'deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline < timezone.now():
            raise forms.ValidationError("Дата должна быть в будущем!")
        return deadline