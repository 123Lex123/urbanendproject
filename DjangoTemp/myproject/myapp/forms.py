from django import forms
from .models import Question, Choice

class PollForm(forms.ModelForm):
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        label="Выберите один из вариантов:"
    )

    class Meta:
        model = Question
        fields = []

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if question:
            self.fields['choice'].queryset = Choice.objects.filter(question=question)
