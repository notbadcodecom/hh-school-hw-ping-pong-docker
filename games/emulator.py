import random
import time
from datetime import datetime


class PingPongEmulator:
    def __init__(self, player1="Игрок А", player2="Игрок Б"):
        self.player1 = player1
        self.player2 = player2
        self.score = [0, 0]
        self.game_number = 0
        self.log = []
        self.current_started_by = None
        self.finished = False
        self.winner = None
        self.games_data = []

    def get_next_server(self):
        if self.game_number == 0:
            return random.choice([self.player1, self.player2])
        current_server = self.games_data[-1]["server"]
        return self.player2 if current_server == self.player1 else self.player1

    def play_game(self):
        self.game_number += 1
        server = self.get_next_server()
        responder = self.player2 if server == self.player1 else self.player1

        self.log.append(f"{server}: ping")

        delay_ms = random.randint(1000, 3000)
        delay_sec = delay_ms / 1000
        time.sleep(delay_ms / 1000)

        self.log.append(f"{responder}: pong ({delay_sec:.2f} с)")

        server_idx = 0 if server == self.player1 else 1
        self.score[server_idx] += 1

        self.log.append(f"Партия {self.game_number}: выиграл {server}")

        self.games_data.append({
            "game_number": self.game_number,
            "server": server,
            "responder": responder,
            "response_time_ms": delay_ms,
            "winner": server
        })

        if self.game_number == 1:
            self.current_started_by = server

    def play_match(self):
        while self.score[0] < 3 and self.score[1] < 3 and self.game_number < 5:
            self.play_game()

        self.finished = True
        if self.score[0] > self.score[1]:
            self.winner = self.player1
        else:
            self.winner = self.player2

        self.log.append("")
        self.log.append(f"Матч завершён! Счёт: {self.player1} {self.score[0]} : {self.score[1]} {self.player2}")
        self.log.append(f"Победитель: {self.winner}")

    def get_status(self):
        return {
            "score": self.score,
            "log": self.log,
            "finished": self.finished,
            "winner": self.winner,
            "games": self.games_data
        }
