from urls import url_paths
from core.app import WebApp, bad_request
from db_assets.db_model import WebsiteDB
from db_assets.db_recipes import COMMENTS
from logger.logger_module import *
from core.render import page_render as render
from views import courses

db_path = 'webserver_db.sqlite'


class AppDb(WebsiteDB):

    @debug
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

    @debug
    def save_comment(self, name, email, subj, text):
        try:
            self.cursor.execute(f"INSERT INTO messages VALUES (Null,'{name}', '{email}', '{subj}', '{text}');")
            self.conn.commit()
        except Exception as e:
            print(e)


# Log().enable_stdout_pipe()
application = WebApp(url_paths, AppDb, db_path, [COMMENTS])


@application.add_route('/create-category/')
def create_category(request, site, db=None):

    if request['method'] == "POST":
        try:
            name = request['queries']['name']
            parent = None
            if 'parent' in request['queries']:
                parent = request['queries']['parent']

            site.create_category(name=name, parent=parent)
            return courses(request=request, site=site)

        except Exception as e:
            print(e)
            return bad_request(request)

    else:

        title = 'Create: Category'
        categories = site.all_categories

        res = render('create_course_or_cat.html', object_list={'title': title,
                                                   'model': 'category',
                                                  'categories': categories})

        return "200 OK", [res]


@application.add_route('/create-course/')
def create_course(request, site, db=None):

    if request['method'] == "POST":
        try:
            type_ = request['queries']['type']
            name = request['queries']['name']
            category = site.get_category_by_id_or_name(id=None, name=request['queries']['category'])

            site.create_course(type_=type_, name=name, category=category)

            return courses(request=request, site=site)
        except Exception as e:
            print(e)
            return bad_request(request)
    else:

        title = 'Create: Course'
        categories = site.all_categories

        res = render('create_course_or_cat.html', object_list={'title': title,
                                                  'model': 'course',
                                                  'categories': categories})

        return "200 OK", [res]
