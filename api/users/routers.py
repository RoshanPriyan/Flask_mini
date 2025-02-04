from flask import Blueprint
from flask_restful import Api
from .views.register_api import register_api
from .views.login_api import login_api
from .views.states_list_api import states_list_api

# Create the Blueprint
router = Blueprint("api", __name__, url_prefix="/api/user")

# Create the API and attach it to the Blueprint
api = Api(router)

# Add function-based API via add_url_rule
router.add_url_rule("/register", view_func=register_api, methods=["POST"])
router.add_url_rule("/login", view_func=login_api, methods=["GET"])
router.add_url_rule("/state-list", view_func=states_list_api, methods=["GET"])
