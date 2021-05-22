from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """set up before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """is information in session and is html displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """check if word is valid"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["K", "I", "T", "E", "S"], 
                                 ["K", "I", "T", "E", "S"], 
                                 ["K", "I", "T", "E", "S"], 
                                 ["K", "I", "T", "E", "S"], 
                                 ["K", "I", "T", "E", "S"]]
        response = self.client.get('/check-word?word=kite')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """check if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=invalid')
        self.assertEqual(response.json['result'], 'not-on-board')

    def check_valid_english_word(self):
        """check if word is a valid english word"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=erggfdgdfgree')
        self.assertEqual(response.json['result'], 'not-word')

