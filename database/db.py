

import sys

sys.path.append('/home/vanek/mark/config')


import psycopg2
from config import db_name, db_password, db_user, db_tables


class Database:
    
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password)

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_tables['users']} (
            id INT not null generated always as identity primary key,
            id_user BIGINT,
            status TEXT,
            language TEXT,
            date_register TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            self.conn.commit()
            
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_tables['users_waiting']} (
            id INT not null generated always as identity primary key,
            id_user BIGINT,
            address TEXT,
            nickname TEXT,
            image TEXT,
            date_register TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            self.conn.commit()
            
    def delete_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(f'''
            DROP TABLE {db_tables['users']} CASCADE;
            ''')
            self.conn.commit()

    def add_user(self, id_user, language):
        with self.conn.cursor() as cur:
            cur.execute(f'''
            INSERT INTO {db_tables['users']} (id_user, status, language)
            VALUES({id_user}, 'member', {repr(language)});
            ''')

            self.conn.commit()
            
    def check_user_db_users(self, id_user):
        with self.conn.cursor() as cur:
            select = f"""
            SELECT id_user
            FROM {db_tables['users']}
            WHERE id_user = {id_user}
            """

            cur.execute(select)
            result = cur.fetchall()
            
            return result
        
        
    def correct_user(self, id_user, language):
        with self.conn.cursor() as cur:
            select = f"""
            SELECT *
            FROM {db_tables['users']}
            WHERE id_user = {id_user}
            """

            cur.execute(select)
            result = cur.fetchall()
            if result == []:
                self.add_user(id_user, language)
                self.conn.commit()
                
    def get_user_language(self, id_user):   
        with self.conn.cursor() as cur:
            select = f"""
            SELECT language
            FROM {db_tables['users']}
            WHERE id_user = {id_user}
            """

            cur.execute(select)
            result = cur.fetchall()
            
            return result
    
    def add_user_wait(self, id_user, address, nickname, image):
        with self.conn.cursor() as cur:
            cur.execute(f'''
            INSERT INTO {db_tables['users_waiting']} (id_user, address, nickname, image)
            VALUES({id_user}, {repr(address)}, {repr(nickname)}, {repr(image)});
            ''')

            self.conn.commit()

    def correct_user_wait(self, id_user, address, nickname, image):
        with self.conn.cursor() as cur:
            select = f"""
            SELECT *
            FROM {db_tables['users_waiting']}
            WHERE id_user = {id_user}
            """

            cur.execute(select)
            result = cur.fetchall()
            if result == []:
                self.add_user_wait(id_user, address, nickname, image)
                self.conn.commit()  
    
    def get_user_status(self, id_user):
        with self.conn.cursor() as cur:
            select = f"""
            SELECT status
            FROM {db_tables['users']}
            WHERE id_user = {id_user}
            """

            cur.execute(select)
            result = cur.fetchall()
            return result
        
    def check_user_wait(self, id_user):
        with self.conn.cursor() as cur:
            select = f"""
            SELECT id_user
            FROM {db_tables['users_waiting']}
            WHERE id_user = {id_user}
            """

            cur.execute(select)
            result = cur.fetchall()
            return result
    
    def delete_user_wait(self, id_user):
        with self.conn.cursor() as cur:
            cur.execute(f"""
            DELETE FROM {db_tables['users_waiting']}
            WHERE id_user = {id_user};
            """)

            self.conn.commit()
                
                
db = Database()
db.create_tables()