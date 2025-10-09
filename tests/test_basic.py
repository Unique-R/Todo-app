import unittest
import os
import sys

# Добавляем путь к приложению
sys.path.insert(0, '/app/app')

class TestBasic(unittest.TestCase):
    
    def test_import_app(self):
        """Test that we can import the app"""
        try:
            from main import app
            self.assertTrue(hasattr(app, 'route'))
        except ImportError as e:
            self.fail(f"Failed to import app: {e}")
    
    def test_environment(self):
        """Test that environment variables are set"""
        self.assertIsNotNone(os.environ.get('DB_HOST'))
        self.assertIsNotNone(os.environ.get('DB_NAME'))

if __name__ == '__main__':
    unittest.main()
