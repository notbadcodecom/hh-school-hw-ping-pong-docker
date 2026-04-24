from django.db import models


class Match(models.Model):
    player1 = models.CharField(max_length=50)
    player2 = models.CharField(max_length=50)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    winner = models.CharField(max_length=50)
    started_by = models.CharField(max_length=50)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.player1} vs {self.player2} ({self.score1}:{self.score2})"


class Game(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='games')
    game_number = models.IntegerField()
    server = models.CharField(max_length=50)
    responder = models.CharField(max_length=50)
    losing_number = models.IntegerField()
    winner = models.CharField(max_length=50)

    class Meta:
        ordering = ['game_number']

    def __str__(self):
        return f"Game {self.game_number} - {self.server} vs {self.responder}"
