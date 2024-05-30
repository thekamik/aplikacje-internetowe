from django import forms
from .models import games, score_table, events
from django.contrib.auth.models import User

class GameForm(forms.ModelForm):
    class Meta:
        model = games
        fields = ['game_name', 'status']
        widgets = {
            'game_name': forms.TextInput(attrs={'max_length': 50}),
        }

class ScoreTableForm(forms.ModelForm):
    class Meta:
        model = score_table
        fields = ['game', 'player', 'player_score']

    def __init__(self, *args, **kwargs):
        super(ScoreTableForm, self).__init__(*args, **kwargs)
        self.fields['game'].queryset = games.objects.all()
        self.fields['game'].label_from_instance = lambda obj: obj.game_name

class EventsForm(forms.ModelForm):
    event_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = events
        fields = ['game', 'event_date', 'event_description']

    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        self.fields['game'].queryset = games.objects.all()
        self.fields['game'].label_from_instance = lambda obj: obj.game_name