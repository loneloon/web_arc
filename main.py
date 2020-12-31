from urls import url_paths
from core.app import WebApp, DebugApp, FakeApp, bad_request
from db_assets.db_model import WebsiteDB
from models import TrainingSite
from logger.logger_module import *
from core.render import page_render as render

db_path = 'sqlite:///webserver_db.db3'


# Log().enable_stdout_pipe()
application = DebugApp(routes=url_paths, db_path=db_path, db_module=WebsiteDB, models=TrainingSite)


# @application.add_route('/create-category/')
# @Log()
# def create_category(request, site, db=None):
#
#     if request['method'] == "POST":
#         try:
#             name = request['queries']['name']
#             parent = None
#             if 'parent' in request['queries']:
#                 parent = request['queries']['parent']
#
#             site.create_category(name=name, parent=parent)
#             return courses(request=request, site=site)
#
#         except Exception as e:
#             print(e)
#             return bad_request(request)
#
#     else:
#
#         title = 'Create: Category'
#         categories = site.all_categories
#
#         res = render('create_category.html', object_list={'title': title,
#                                                    'model': 'category',
#                                                   'categories': categories})
#
#         return "200 OK", [res]
#
#
# @application.add_route('/create-course/')
# @Log()
# def create_course(request, site, db=None):
#
#     if request['method'] == "POST":
#         try:
#             type_ = request['queries']['type']
#             name = request['queries']['name']
#             category = site.get_category_by_id_or_name(id=None, name=request['queries']['category'])
#
#             site.create_course(type_=type_, name=name, category=category)
#
#             return courses(request=request, site=site)
#         except Exception as e:
#             print(e)
#             return bad_request(request)
#     else:
#
#         title = 'Create: Course'
#         categories = site.all_categories
#
#         res = render('create_category.html', object_list={'title': title,
#                                                   'model': 'course',
#                                                   'categories': categories})
#
#         return "200 OK", [res]
