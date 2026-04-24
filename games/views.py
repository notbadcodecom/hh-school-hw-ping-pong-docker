from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status as rest_status
from django.core.cache import cache
from django.utils import timezone
from threading import Thread
from datetime import datetime
import time
import random

from .models import Match, Game
from .serializers import MatchSerializer
from .emulator import PingPongEmulator

ACTIVE_MATCHES = {}


def index(request):
    return render(request, 'games/index.html')


@csrf_exempt
@require_http_methods(["POST"])
def start_match(request):
    match_id = f"match_{int(datetime.now().timestamp() * 1000)}"

    match_state = {
        'match_id': match_id,
        'player1': 'Ma Long',
        'player2': 'Jan-Ove Waldner',
        'score': [0, 0],
        'game_number': 0,
        'log': [],
        'finished': False,
        'winner': None,
        'games': []
    }

    ACTIVE_MATCHES[match_id] = match_state

    def run_match():
        try:
            started_by = None
            match_wins = [0, 0]

            for game_num in range(1, 6):
                match_state['game_number'] = game_num

                if game_num == 1:
                    server = random.choice([match_state['player1'], match_state['player2']])
                    started_by = server
                else:
                    last_server = match_state['games'][-1]['server']
                    server = match_state['player2'] if last_server == match_state['player1'] else match_state['player1']

                responder = match_state['player2'] if server == match_state['player1'] else match_state['player1']

                losing_number = random.randint(3, 9)
                counter = 0
                last_player = None

                match_state['log'].append(f"Партия {game_num}")

                while counter < losing_number:
                    counter += 1

                    if counter % 2 == 1:
                        current_player = server
                        action = "ping"
                    else:
                        current_player = responder
                        action = "pong"

                    last_player = current_player
                    match_state['log'].append(f"{current_player}: {action}")

                    delay_ms = random.randint(1000, 2000)
                    time.sleep(delay_ms / 1000)

                next_player = responder if last_player == server else server
                match_state['log'].append(f"{next_player}: oops")

                winner = last_player
                winner_idx = 0 if winner == match_state['player1'] else 1
                match_wins[winner_idx] += 1
                match_state['score'] = match_wins

                match_state['log'].append(f"Партия {game_num}: выиграл {winner}")
                match_state['log'].append("")

                match_state['games'].append({
                    'game_number': game_num,
                    'server': server,
                    'responder': responder,
                    'losing_number': losing_number,
                    'winner': winner
                })

                if match_wins[0] == 3 or match_wins[1] == 3:
                    break

            match_state['finished'] = True
            if match_state['score'][0] > match_state['score'][1]:
                match_state['winner'] = match_state['player1']
            else:
                match_state['winner'] = match_state['player2']

            match_state['log'].append('')
            match_state['log'].append(f"🏆 Матч завершён! Счёт: {match_state['player1']} {match_state['score'][0]} : {match_state['score'][1]} {match_state['player2']}")
            match_state['log'].append(f"👑 Победитель матча: {match_state['winner']}")

            match_obj = Match.objects.create(
                player1=match_state['player1'],
                player2=match_state['player2'],
                score1=match_state['score'][0],
                score2=match_state['score'][1],
                winner=match_state['winner'],
                started_by=started_by,
                end_time=timezone.now()
            )

            for game_data in match_state['games']:
                Game.objects.create(
                    match=match_obj,
                    game_number=game_data['game_number'],
                    server=game_data['server'],
                    responder=game_data['responder'],
                    losing_number=game_data['losing_number'],
                    winner=game_data['winner']
                )
        except Exception as e:
            print(f"Error in match thread: {e}")
            match_state['finished'] = True
            match_state['log'].append(f"Ошибка: {str(e)}")

    thread = Thread(target=run_match)
    thread.daemon = True
    thread.start()

    return JsonResponse({'match_id': match_id})


@csrf_exempt
@require_http_methods(["GET"])
def match_status(request, match_id):
    match_state = ACTIVE_MATCHES.get(match_id)

    if not match_state:
        return JsonResponse({'error': 'Match not found'}, status=404)

    return JsonResponse({
        'is_finished': match_state['finished'],
        'score': match_state['score'],
        'current_log': match_state['log'],
        'winner': match_state['winner']
    })


@csrf_exempt
@require_http_methods(["GET"])
def matches_list(request):
    matches = Match.objects.all()
    serializer = MatchSerializer(matches, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@require_http_methods(["DELETE"])
def clear_matches(request):
    Match.objects.all().delete()
    return JsonResponse({'status': 'success'})
