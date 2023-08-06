import os
import os.path as osp
import logging

import connexion
from flask_sqlalchemy import SQLAlchemy  # TODO: remove
from flask_marshmallow import Marshmallow  # TODO: remove
from flask_cors import CORS

from .util import rand_string

log = logging.getLogger("PaddleLabel")

basedir = osp.abspath(osp.dirname(__file__))

db_path = f"{osp.join(os.path.expanduser('~'), '.paddlelabel', 'paddlelabel.db')}"

if not osp.exists(osp.dirname(db_path)):
    os.makedirs(osp.dirname(db_path))
db_url = f"sqlite:///{db_path}"
print(f"Database path: {db_url}")

connexion_app = connexion.App("PaddleLabel")
app = connexion_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = rand_string(30)

app.static_url_path = "/static"
app.static_folder = osp.join(basedir, "static")
CORS(connexion_app.app)

db = SQLAlchemy(app)
se = db.session
ma = Marshmallow(app)
db_head_version = "a609821ce310"

# reject requests with the same request_id within request_id_timeout seconds
request_id_timeout = 2

data_base_dir = osp.join(os.path.expanduser("~"), ".paddlelabel")
