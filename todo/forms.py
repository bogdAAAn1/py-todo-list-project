from django import forms
from todo.models import Tag, Task


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'YYYY-MM-DD HH:MM'
        },
            format='%Y-%m-%dT%H:%M'
        ),
        required=False
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ["content", "deadline", "is_done", "tag"]
