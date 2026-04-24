from django.test import TestCase, Client
from django.urls import reverse
from .models import Match, Game
import json


class PingPongEmulatorTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_start_match_returns_match_id(self):
        response = self.client.post(reverse('games:start_match'),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('match_id', data)

    def test_match_status_initial_state(self):
        start_response = self.client.post(reverse('games:start_match'),
                                         content_type='application/json')
        match_id = json.loads(start_response.content)['match_id']

        status_response = self.client.get(
            reverse('games:match_status', kwargs={'match_id': match_id})
        )
        self.assertEqual(status_response.status_code, 200)
        data = json.loads(status_response.content)

        self.assertFalse(data['is_finished'])
        self.assertEqual(data['score'], [0, 0])

    def test_match_completes(self):
        import time
        start_response = self.client.post(reverse('games:start_match'),
                                         content_type='application/json')
        match_id = json.loads(start_response.content)['match_id']

        time.sleep(15)

        status_response = self.client.get(
            reverse('games:match_status', kwargs={'match_id': match_id})
        )
        data = json.loads(status_response.content)

        self.assertTrue(data['is_finished'])
        self.assertIsNotNone(data['winner'])
        self.assertTrue(max(data['score']) == 3)

    def test_match_saved_to_database(self):
        import time
        self.client.post(reverse('games:start_match'),
                        content_type='application/json')
        time.sleep(15)

        matches = Match.objects.all()
        self.assertEqual(matches.count(), 1)

        match = matches.first()
        self.assertEqual(match.player1, 'Ma Long')
        self.assertEqual(match.player2, 'Jan-Ove Waldner')
        self.assertIsNotNone(match.winner)
        self.assertEqual(match.score1 + match.score2, match.games.count())

    def test_matches_list(self):
        response = self.client.get(reverse('games:matches_list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)

    def test_clear_matches(self):
        Match.objects.create(
            player1='Test 1',
            player2='Test 2',
            score1=3,
            score2=1,
            winner='Test 1',
            started_by='Test 1'
        )

        self.assertEqual(Match.objects.count(), 1)

        self.client.delete(reverse('games:clear_matches'))

        self.assertEqual(Match.objects.count(), 0)
