import unittest
import sqlite3
import os
from app import app

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test_database.db'
        self.client = app.test_client()
        
        if os.path.exists(app.config['DATABASE']):
            os.remove(app.config['DATABASE'])
            
        with app.app_context():
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    is_completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()

    def tearDown(self):
        if os.path.exists(app.config['DATABASE']):
            os.remove(app.config['DATABASE'])

    def test_index_empty(self):
        """1. GET / - 빈 목록 확인"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Todo List', response.data)

    def test_add_todo_normal(self):
        """2. POST /add - 정상 제목 추가"""
        response = self.client.post('/add', data={'title': '  Test Task  '}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

    def test_add_todo_whitespace_only(self):
        """3. POST /add - 공백만 있는 제목 (저장 안 되어야 함)"""
        # 1. 초기 상태 확인 (데이터 1개 삽입)
        with app.app_context():
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.execute("INSERT INTO todos (title) VALUES ('Existing')")
            conn.commit()
            conn.close()

        # 2. 빈 제목(공백) 추가 시도
        self.client.post('/add', data={'title': '   '}, follow_redirects=True)

        # 3. DB에 데이터가 여전히 1개인지 확인
        with app.app_context():
            conn = sqlite3.connect(app.config['DATABASE'])
            count = conn.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
            conn.close()
        
        self.assertEqual(count, 1, "공백만 있는 제목은 저장되지 않아야 합니다.")

    def test_add_todo_long_title(self):
        """4. POST /add - 긴 제목 추가"""
        long_title = "A" * 150
        response = self.client.post('/add', data={'title': long_title}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(long_title.encode(), response.data)

    def test_list_after_addition(self):
        """5. GET / - 추가 후 목록 확인"""
        self.client.post('/add', data={'title': 'Task 1'})
        self.client.post('/add', data={'title': 'Task 2'})
        response = self.client.get('/')
        self.assertIn(b'Task 1', response.data)
        self.assertIn(b'Task 2', response.data)

if __name__ == '__main__':
    unittest.main()

import unittest
import sqlite3
import os
from app import app

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        # 테스트용 설정
        app.config['TESTING'] = True
        # 메모리 DB 대신 테스트 전용 파일 DB 사용 (연결 간 데이터 공유를 위해)
        app.config['DATABASE'] = 'test_database.db'
        self.client = app.test_client()
        
        # 기존 테스트 DB 파일이 있다면 삭제
        if os.path.exists(app.config['DATABASE']):
            os.remove(app.config['DATABASE'])
            
        # 새로운 테스트 DB 생성 및 테이블 초기화
        with app.app_context():
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    is_completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()

    def tearDown(self):
        # 테스트 종료 후 테스트 DB 파일 삭제
        if os.path.exists(app.config['DATABASE']):
            os.remove(app.config['DATABASE'])

    def test_index_empty(self):
        """1. GET / - 빈 목록 확인"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Todo List', response.data)

    def test_add_todo_normal(self):
        """2. POST /add - 정상 제목 추가"""
        response = self.client.post('/add', data={'title': '  Test Task  '}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

    def test_add_todo_whitespace_only(self):
        """3. POST /add - 공백만 있는 제목 (저장 안 되어야 함)"""
        # 먼저 하나를 넣어둠으로써 목록이 비어있지 않음을 보장
        with app.app_context():
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.execute("INSERT INTO todos (title) VALUES ('Existing')")
            conn.commit()
            conn.close()

        response = self.client.post('/add', data={'title': '   '}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Existing', response.data)
        self.assertNotIn(b'   ', response.data)

    def test_add_todo_long_title(self):
        """4. POST /add - 긴 제목 추가"""
        long_title = "A" * 150
        response = self.client.post('/add', data={'title': long_title}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(long_title.encode(), response.data)

    def test_list_after_addition(self):
        """5. GET / - 추가 후 목록 확인"""
        self.client.post('/add', data={'title': 'Task 1'})
        self.client.post('/add', data={'title': 'Task 2'})
        response = self.client.get('/')
        self.assertIn(b'Task 1', response.data)
        self.assertIn(b'Task 2', response.data)

if __name__ == '__main__':
    unittest.main()

import unittest
import os
import sqlite3
from app import app, init_db

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        # 테스트용 설정
        app.config['TESTING'] = True
        app.config['DATABASE'] = ':memory:'
        self.client = app.test_client()
        
        # 메모리 DB 초기화 (app.py의 init_db가 app.config를 참조하므로 직접 수행)
        # 다만 app.py 내부의 get_db_connection이 이미 실행된 후라면 
        # app.config를 바꾸는 것만으로 충분할 수 있음.
        # 메모리 DB는 연결할 때마다 새로 생성되므로, 
        # 테스트 함수마다 새로운 연결을 만들어야 함.
        
        # 테스트용 DB 초기화를 위한 별도의 setup logic
        with app.app_context():
            # app.py의 init_db를 호출하여 메모리 DB에 테이블 생성
            # app.py의 get_db_connection이 app.config['DATABASE']를 사용하도록 되어 있음
            # 메모리 DB는 연결(connection)이 닫히면 사라지므로, 
            # 테스트 클라이언트가 매번 새 연결을 맺을 때마다 테이블을 만들어줘야 함.
            pass

    def tearDown(self):
        pass

    def create_test_db(self):
        """테스트를 위한 메모리 DB 초기화 함수"""
        # Flask의 app_context를 사용하여 연결 및 테이블 생성
        with app.app_context():
            import sqlite3
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    is_completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()

    def test_index_empty(self):
        """1. GET / - 빈 목록 확인"""
        self.create_test_db()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Todo List', response.data)

    def test_add_todo_normal(self):
        """2. POST /add - 정상 제목 추가"""
        self.create_test_db()
        response = self.client.post('/add', data={'title': '  Test Task  '}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

    def test_add_todo_whitespace_only(self):
        """3. POST /add - 공백만 있는 제목 (저장 안 되어야 함)"""
        self.create_test_db()
        # 먼저 하나를 넣어둠으로써 목록이 비어있지 않음을 보장
        with app.app_context():
            import sqlite3
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.execute("INSERT INTO todos (title) VALUES ('Existing')")
            conn.commit()
            conn.close()

        response = self.client.post('/add', data={'title': '   '}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # 'Existing'은 있어야 하지만 새로 들어간 '   '는 없어야 함
        self.assertIn(b'Existing', response.data)
        self.assertNotIn(b'   ', response.data)

    def test_add_todo_long_title(self):
        """4. POST /add - 긴 제목 추가"""
        self.create_test_db()
        long_title = "A" * 150
        response = self.client.post('/add', data={'title': long_title}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(long_title.encode(), response.data)

    def test_list_after_addition(self):
        """5. GET / - 추가 후 목록 확인"""
        self.create_test_db()
        self.client.post('/add', data={'title': 'Task 1'})
        self.client.post('/add', data={'title': 'Task 2'})
        response = self.client.get('/')
        self.assertIn(b'Task 1', response.data)
        self.assertIn(b'Task 2', response.data)

if __name__ == '__main__':
    unittest.main()
