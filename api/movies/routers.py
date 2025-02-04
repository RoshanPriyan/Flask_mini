from flask import Blueprint
from flask_restful import Api
from api.movies.views.movie_register_api import movie_register_api, movie_list_api
from api.movies.views.add_theater_api import register_theater_api
from api.movies.views.book_movie_api import book_movie_api
from api.movies.views.available_seta import available_ticket_api
from api.movies.views.theater_seat import theater_seat_api
from api.movies.views.book_seat import book_seat_api


router = Blueprint("movie", __name__, url_prefix="/api/movie")
api = Api(router)


router.add_url_rule("/register-movie", view_func=movie_register_api, methods=["POST"])
router.add_url_rule("/movie-list", view_func=movie_list_api, methods=["GET"])
router.add_url_rule("/add-theater", view_func=register_theater_api, methods=["POST"])
router.add_url_rule("/book", view_func=book_movie_api, methods=["POST"])
router.add_url_rule("/available-seat", view_func=available_ticket_api, methods=["GET"])
router.add_url_rule("/theater-seat", view_func=theater_seat_api, methods=["GET"])
router.add_url_rule("/book-seat", view_func=book_seat_api, methods=["POST"])
