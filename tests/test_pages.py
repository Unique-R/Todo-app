import unittest
import os
import sys
from main import app

# Добавляем путь к приложению
sys.path.insert(0, '/app/app')

class TestPages(unittest.TestCase):
    
    def test_home_page_redirects_to_login(self):
        """Test that home page redirects to login when not authenticated"""
        with app.test_client() as client:
            response = client.get('/')
            # Должен перенаправить на /login если не залогинен
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login', response.location)
    
    def test_login_page_works(self):
        """Test that login page returns 200 OK"""
        with app.test_client() as client:
            response = client.get('/login')
            self.assertEqual(response.status_code, 200)
    
    def test_register_page_works(self):
        """Test that register page returns 200 OK"""
        with app.test_client() as client:
            response = client.get('/register')
            self.assertEqual(response.status_code, 200)
    
    def test_can_add_task(self):
        """Test that we can add a task (simulate logged in user)"""
        with app.test_client() as client:
            # Создаем сессию как будто пользователь залогинен
            with client.session_transaction() as session:
                session['user_id'] = 1
                session['username'] = 'testuser'
            
            response = client.post('/add', data={'task': 'CI/CD Test Task'})
            # Должен перенаправить на главную после добавления
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')

if __name__ == '__main__':
    unittest.main()
