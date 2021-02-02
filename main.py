from urls import url_paths
from core.app import WebApp, DebugApp, FakeApp, bad_request
from db_assets.db_model import WebsiteDB
from models import TrainingSite

db_path = 'sqlite:///webserver_db.db3'

# Uncomment for non-Debug version
# application = WebApp(routes=url_paths, db_path=db_path, db_module=WebsiteDB, models=TrainingSite)
application = DebugApp(routes=url_paths, db_path=db_path, db_module=WebsiteDB, models=TrainingSite)

