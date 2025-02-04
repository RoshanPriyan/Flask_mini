from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from api.users.routers import router as user_router
from api.movies.routers import router as movie_router

load_dotenv()

host = os.getenv("FLASKHOST")
port = os.getenv("FLASKPORT")
debug = os.getenv("DEBUG")

app = Flask(__name__)
# Register the Blueprint
app.register_blueprint(user_router)
app.register_blueprint(movie_router)


CORS(app) 

if __name__=="__main__":
    app.run(host=host, port=port, debug=debug)
