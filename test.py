from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="instructions">',html)

    def test_new_game(self):
        with app.test_client() as client:
            resp = client.get('/new-game')
            html = resp.get_data(as_text=True)

            self.assertIn('boggle_board',session)
            self.assertEqual(session['high_score'], 0)
            self.assertEqual(session['times_played'], 0)
            

    def test_play_game(self):
        with app.test_client() as client:
            resp = client.get('/play')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div id="scoreboard">',html)


    def test_check_word(self):
        with app.test_client() as client:
            resp = client.get('/check-word')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_game_over(self):
        with app.test_client() as client:
            resp = client.get('/game-over')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)