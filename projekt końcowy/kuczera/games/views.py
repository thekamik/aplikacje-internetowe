from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import games, score_table, events
from .forms import GameForm, ScoreTableForm, EventsForm

# Create your views here.
def index(request):
    return render(request, "index.html")

def games_view(request):
    # return render(request, "games.html")
    all_games = games.objects.all()
    form = GameForm()
    edit_game = None

    if request.method == 'POST' and request.user.is_staff:

        # Zmienne odczytywane ze strony
        delete_game = request.POST.get('delete_game') == 'true' # Naciśnięto przycisk delete
        edit_game = request.POST.get('edit_game') == 'true' # Naciśnięty został przycisk edycji
        game_id = request.POST.get('game_id') # Pokazuje poprawne Id tylko po wciśnięciu przycisków Edit lub Delete
        apply_changes = request.POST.get('apply_changes') == 'true' # Aktywna jest forma modyfikacji strony, jeżeli false to aktywna jest forma dodaj nowe

        # jeżli wywołany został tryb edycji, to zapisz numer edytowanej gry w danych sesji
        if edit_game:
            request.session['game_id'] = game_id

        # Usuwanie elementu z bazy danych
        if delete_game: 
            print("Delete game")
            game = get_object_or_404(games, id=game_id)
            game.delete()
            return redirect('games')
        
        # Dodanie lub modyfikacja elementu bazy danych
        form = GameForm(request.POST)
        if form.is_valid():
            new_game = form.save(commit=False)
            new_game.last_update = timezone.now()

            if apply_changes:
                # Jeżeli obiekt jest modyfikowany to wykonaj to
                game = get_object_or_404(games, id=request.session['game_id'])
                new_game.creation_date = game.creation_date
                new_game.id = request.session['game_id']
            else:
                # Jeżeli jest to nowy obiekt to wykonaj to
                new_game.creation_date = timezone.now()
            new_game.last_update = timezone.now()
            new_game.save()
            return redirect('games')

    return render(request, 'games.html', {'games': all_games, 'form': form, 'edit_game': edit_game})


def scoreboard_view(request):
    all_scores = score_table.objects.select_related('game').all()
    form = ScoreTableForm()

    if request.method == 'POST' and request.user.is_staff:

        # Pobierz zmienne ze strony
        delete_entry = request.POST.get('delete_entry') == 'true' # Naciśnięto przycisk delete
        score_id = request.POST.get('score_id')

        # obsłuż usunięcie elementu z bazy danych
        if delete_entry:
            score_entry = get_object_or_404(score_table, id=score_id)
            score_entry.delete()
            redirect('scoreboard')

        form = ScoreTableForm(request.POST)
        if form.is_valid():
            new_score = form.save(commit=False)
            new_score.score_date = timezone.now()
            new_score.save()
            return redirect('scoreboard')

    return render(request, 'scoreboard.html', {'all_scores': all_scores, 'form': form})


def events_view(request):
    all_events = events.objects.select_related('game').all()
    form = EventsForm()

    if request.method == 'POST' and request.user.is_staff:

        # Pobierz zmienne ze strony
        delete_event = request.POST.get('delete_event') == 'true' # Naciśnięto przycisk delete
        event_id = request.POST.get('event_id')

        # obsłuż usunięcie elementu z bazy danych
        if delete_event:
            print("DEBUG: ", event_id)
            event_entry = get_object_or_404(events, id=event_id)
            event_entry.delete()
            redirect('events')
    
        form = EventsForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.save()
            return redirect('events')

    return render(request, 'events.html', {'all_events': all_events, 'form': form})
