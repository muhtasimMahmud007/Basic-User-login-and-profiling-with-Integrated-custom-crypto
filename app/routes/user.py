from ..controllers.user_controller import UserController
from flask import Blueprint

user = Blueprint("user", __name__, template_folder="../views")
controller = UserController()

user.route("/profile", methods=["GET"])(controller.profile)
