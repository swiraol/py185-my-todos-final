from contextlib import contextmanager 

import logging
import psycopg2
from psycopg2.extras import DictCursor 

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class DatabasePersistence:
    def __init__(self):
        pass
    @contextmanager
    def _database_connect(self):
        connection = psycopg2.connect(dbname='todos')

        try:
            with connection:
                yield connection
        finally:
            connection.close()
    
    def find_list(self, list_id):
        query = 'SELECT * FROM lists WHERE id = %s'
        logger.info("Executing query: %s with list_id: %s", query, list_id)
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (list_id,))
                lst = dict(cursor.fetchone())
        lst.setdefault('todos', [])
        lst['todos'] = lst['todos'] + self._find_todos_for_list(list_id)
        return lst  
    
    def all_lists(self):
        query = 'SELECT * FROM lists'
        logger.info("Executing query: %s", query)
        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        lists = [dict(result) for result in results]
        for lst in lists:
            todos = self._find_todos_for_list(lst['id'])
            lst.setdefault('todos', todos)

        return lists

    def create_new_list(self, title):
        query = "INSERT INTO lists (title) VALUES (%s)"
        logger.info("Executing query: %s with title: %s", query, title)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (title,))

    def update_list_by_id(self, list_id, new_title):
        query = "UPDATE lists SET title = %s WHERE id = %s"
        logger.info("Executing query: %s with new_title: %s and id: %s", query, new_title, list_id)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (new_title, list_id))
    
    def delete_list(self, list_id):
        query = "DELETE FROM lists WHERE id = %s"
        logger.info("Executing query: %s with id: %s", query, list_id)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (list_id,))

    def create_new_todo(self, list_id, todo_title):
        query = "INSERT INTO todos (list_id, title) VALUES(%s, %s)"
        logger.info("Executing query: %s with list_id: %s and title %s",
                    query, list_id, todo_title)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (list_id, todo_title,))

    # Code omitted for brevity
    # def create_new_todo(self, list_id, todo_title):
    #     query = "INSERT INTO todos (list_id, title) VALUES (%s, %s)"
    #     logger.info("Executing query: %s with id: %s and title: %s", query, list_id, todo_title)
    #     with self._database_connect() as conn:
    #         with conn.cursor() as cursor:
    #             cursor.execute(query, (list_id, todo_title))

    def delete_todo_from_list(self, list_id, todo_id):
        pass
    
    def update_todo_status(self, list_id, todo_id, new_status):
        pass
    
    def mark_all_todos_completed(self, list_id):
        pass

    def _find_todos_for_list(self, list_id):
        query = 'SELECT * FROM todos WHERE list_id = %s'
        logger.info('Execute query: %s with list_id: %s', query, list_id)
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (list_id,))
                return cursor.fetchall()