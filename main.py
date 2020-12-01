from urls import url_paths
from core.app import WebApp
from db_assets.db_model import WebsiteDB
from db_assets.db_recipes import COMMENTS

db_path = 'webserver_db.sqlite'


class AppDb(WebsiteDB):

    def load_comments(self):
        try:
            self.cursor.execute("SELECT * FROM messages;")
            result = self.cursor.fetchall()
            if not result:
                return []
            else:
                return result
        except Exception as e:
            print(e)
            return []

    def save_comment(self, name, email, subj, text):
        try:
            self.cursor.execute(f"INSERT INTO messages VALUES (Null,'{name}', '{email}', '{subj}', '{text}');")
            self.conn.commit()
        except Exception as e:
            print(e)


application = WebApp(url_paths, AppDb, db_path, [COMMENTS])
