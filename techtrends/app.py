"""
Techtrends Flask application.

"""
import logging

from logger import configure_logging
from utils.database import DatabaseConnection

from flask import (
    Flask,
    jsonify,
    json,
    render_template,
    request,
    url_for,
    redirect,
    flash,
)

from typing import Any, List, Dict
from sqlite3 import OperationalError
from werkzeug.exceptions import abort

# Define the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"
database = DatabaseConnection(database_name="database.db")


@app.route("/")
def index():
    """
    Define the main route of the web application.
    """
    try:
        posts = database.execute("SELECT * FROM posts")

    except OperationalError as e:
        logging.error(f"Database error. Route: {request.url_rule}")
        return render_template("500.html", error=e), 500

    logging.info("Showing the Landing page.")
    return render_template("index.html", posts=posts)


@app.route("/healthz")
def health_probe():
    """Health probe endpoint for the app."""

    try:
        database.execute("SELECT * FROM posts")
        response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype="application/json",
        )
        logging.info("Showing the health page.")

    except OperationalError as e:
        response = app.response_class(
            response=json.dumps({"result": "ERROR - unhealthy - Database Error"}),
            status=500,
            mimetype="application/json",
        )
        logging.error(f"Database error. Route: {request.url_rule}")

    except Exception as e:
        response = app.response_class(
            response=json.dumps({"result": "ERROR - unhealthy - Unknown Error"}),
            status=500,
            mimetype="application/json",
        )
        logging.error(f"Unknown error. Route: {request.url_rule}")

    return response


@app.route("/metrics")
def app_metrics():
    try:
        posts = database.execute("SELECT * FROM posts")
        response = app.response_class(
            response=json.dumps(
                {
                    "status": "Healthy",
                    "database_requests": database.DATABASE_CONNECTION_COUNT,
                    "count_post": len(posts),
                }
            ),
            status=200,
            mimetype="application/json",
        )
        logging.info(f"Showing Metrics page. Route: {request.url_rule}")

    except OperationalError as e:
        response = app.response_class(
            response=json.dumps({"result": "ERROR - unhealthy - Database Error"}),
            status=500,
            mimetype="application/json",
        )
        logging.error(f"Database Error. Route: {request.url_rule}")

    except Exception as e:
        response = app.response_class(
            response=json.dumps({"result": "ERROR - unhealthy - Unknown Error"}),
            status=500,
            mimetype="application/json",
        )
        logging.error(f"Unknown Error. Route: {request.url_rule}")

    return response


@app.route("/<int:post_id>")
def post(post_id):
    """
    Retrieve a single post from database.
    If the post ID is not found a 404 page is shown.
    """
    try:
        post = database.get_post(post_id)
        if len(post) == 0:
            logging.warning(
                f"Article with id {post_id} does not exist. Route: {request.url_rule}"
            )
            return render_template("404.html"), 404

    except OperationalError as e:
        logging.error(f"Database Error. Route: {request.url_rule}")
        return render_template("500.html", error=e), 500

    logging.info(f"Article with id '{post[0][0]}' and title '{post[0][2]}' retrieved")
    return render_template("post.html", post=post[0])


@app.route("/about")
def about():
    """
    Define the about us page.
    """
    logging.info("About Us page retrieved")
    return render_template("about.html")


# Define the post creation functionality
@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            try:
                database.execute(
                    f"INSERT INTO \
                    posts (title, content) VALUES (?, ?)",
                    (title, content),
                )
                logging.info(f"Article with title '{title}' created.")
                return redirect(url_for("index"))

            except OperationalError as e:
                logging.error(f"Database Error. Route: {request.url_rule}")
                return render_template("500.html", error=e), 500

            except Exception as e:
                logging.error(f"Unknown Error. Route: {request.url_rule}")
                return render_template("500.html", error=e), 500

    # TODO: handle title/content not provided
    return render_template("create.html")


# start the application on port 3111
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3111")
