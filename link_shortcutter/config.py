import os

import dotenv

dotenv.load_dotenv()

mongo_url = os.getenv("db_url", "localhost")
db_name = os.getenv("db_name", "links_db")
links_collection_name = os.getenv("links_collection_name", "links")

_templates_dirname = "templates"
templates_path = os.path.join(os.path.dirname(__file__), _templates_dirname)
