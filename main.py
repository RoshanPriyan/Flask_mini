from flask import Flask
import os
from dotenv import load_dotenv
from api.users.routers import router as user_router
from api.movies.routers import router as movie_router

load_dotenv()

debug = os.getenv("DEBUG")

app = Flask(__name__)
# Register the Blueprint
app.register_blueprint(user_router)
app.register_blueprint(movie_router)


if __name__=="__main__":
    app.run(debug=debug)
