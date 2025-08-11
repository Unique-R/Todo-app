import unittest
from main import app  # Предполагая, что main.py — это твой файл

class TestToDoApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')

if __name__ == '__main__':
    unittest.main()
