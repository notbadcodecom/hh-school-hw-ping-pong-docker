from rest_framework import serializers
from .models import Match, Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_number', 'server', 'responder', 'losing_number', 'winner']


class MatchSerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'player1', 'player2', 'score1', 'score2', 'winner',
                  'started_by', 'start_time', 'end_time', 'games']


class MatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'player1', 'player2', 'score1', 'score2', 'winner',
                  'started_by', 'start_time', 'end_time']
