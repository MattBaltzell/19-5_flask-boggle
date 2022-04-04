from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    
    # TODO -- write tests for every view function / feature!

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_home_page(self):
        """Check for rendered home page template"""
        with self.client:
            resp = self.client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="instructions">',html)


    def test_new_game(self):
        """Check for correct new game setup from session and successful redirect"""
        with self.client:
            resp = self.client.get('/new-game')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/play')
            self.assertIn('boggle_board',session)
            self.assertIn('high_score',session)
            self.assertEqual(session['high_score'], 0)
            self.assertNotIn('times_played', session)


    def test_play_game(self):
        """Check for rendered game template"""
        with self.client:
            resp = self.client.get('/play')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div id="scoreboard">',html)


    def test_valid_word(self):
        """Check for word on the board and in the dictionary"""
        with self.client as client:
            with client.session_transaction() as session:
                session['boggle_board'] = [['A','A','A','A','A'],
                                    ['A','T','B','A','A'],
                                    ['A','S','A','D','A'],
                                    ['A','A','R','S','A'],
                                    ['A','A','A','A','K']]
            
        response = self.client.get('/check-word?word=sad')
        self.assertEqual(response.json['result'], 'ok')

        response = self.client.get('/check-word?word=task')
        self.assertEqual(response.json['result'], 'ok')

        response = self.client.get('/check-word?word=bar')
        self.assertEqual(response.json['result'], 'ok')

        response = self.client.get('/check-word?word=bat')
        self.assertEqual(response.json['result'], 'ok')  

    
    def test_offboard_word(self):
        """Check for real word, not on board"""
        self.client.get('/new-game')
        response =self.client.get('/check-word?word=dimple')
        self.assertEqual(response.json['result'], 'not-on-board')


    def test_invalid_word(self):
        """Check for word not in the dictionary"""
        self.client.get('/new-game')
        response =self.client.get('/check-word?word=sippindasizzurp')
        self.assertEqual(response.json['result'], 'not-word')  


    # def test_game_over(self):
    #     with app.test_client() as client:
    #         resp = client.post('/game-over', data={'result': 0})
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200) 
    #         self.assertEqual(resp.json['result'], 0)