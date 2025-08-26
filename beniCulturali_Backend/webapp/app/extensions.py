from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

# this file is for tool and extension initialization
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

# avoiding circular imports by separating extensions into their own file
