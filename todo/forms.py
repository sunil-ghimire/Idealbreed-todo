from .models import TodoModel
from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model = TodoModel
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Add task here...',
                }
            )
        }
