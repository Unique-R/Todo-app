import unittest
import os
import sys
import psycopg2
import subprocess

# Добавляем путь к приложению
sys.path.insert(0, '/app/app')

class TestDatabase(unittest.TestCase):
    
    def test_database_connection(self):
        """Test that we can connect to the database"""
        try:
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST'),
                database=os.environ.get('DB_NAME'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD')
            )
            # Проверяем что можем выполнить запрос
            cur = conn.cursor()
            cur.execute('SELECT 1')
            result = cur.fetchone()
            self.assertEqual(result[0], 1)
            
            cur.close()
            conn.close()
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
    
    def test_replication_working(self):
        """Test that database replication is working"""
        try:
            # Проверяем что реплика в режиме только для чтения
            result = subprocess.run([
                'docker', 'exec', 'todo-db-replica-1', 
                'psql', '-U', 'postgres', '-c', "SELECT pg_is_in_recovery();"
            ], capture_output=True, text=True, timeout=30)
            
            # 't' означает что реплика работает в режиме recovery
            self.assertIn('t', result.stdout)
        except subprocess.TimeoutExpired:
            self.fail("Replica check timed out")
        except Exception as e:
            self.fail(f"Replication test failed: {e}")

if __name__ == '__main__':
    unittest.main()
