import os
from flask import Flask, flash, redirect, render_template, request, url_for
from classifier import ProblemClassifier
from database import init_db, create_service_request, get_service_requests

BASE = os.path.dirname(os.path.abspath(__file__))

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "local-week2-key"),
        DATABASE=os.environ.get("SERVICE_REQUEST_DB", os.path.join(BASE, "service_requests_week2.db")),
        TRAINING_DATA=os.path.join(BASE, "sample_training_data.csv"),
    )
    if test_config:
        app.config.update(test_config)
    init_db(app.config["DATABASE"])
    model = ProblemClassifier(app.config["TRAINING_DATA"])
    app.extensions["problem_classifier"] = model

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.route("/requests/new", methods=["GET", "POST"])
    def new_request():
        if request.method == "GET":
            return render_template("new_request.html", categories=model.categories)
        description = request.form.get("description", "").strip()
        chosen = request.form.get("category", "").strip() or None
        if len(description) < 8:
            flash("Enter a description with at least 8 characters.", "error")
            return render_template("new_request.html", categories=model.categories,
                                   description=description, chosen=chosen), 400
        if len(description) > 1000:
            flash("Description must be 1,000 characters or fewer.", "error")
            return render_template("new_request.html", categories=model.categories,
                                   description=description, chosen=chosen), 400
        if chosen and chosen not in model.categories:
            flash("Choose a valid category.", "error")
            return render_template("new_request.html", categories=model.categories,
                                   description=description), 400
        predicted, confidence = model.predict(description)
        final_category = chosen or predicted
        new_id = create_service_request(app.config["DATABASE"], description,
                                        predicted, final_category, confidence)
        return redirect(url_for("request_detail", request_id=new_id))

    @app.get("/requests")
    def requests_page():
        return render_template("requests.html",
                               requests=get_service_requests(app.config["DATABASE"]))

    @app.get("/requests/<int:request_id>")
    def request_detail(request_id):
        rows = get_service_requests(app.config["DATABASE"])
        item = next((row for row in rows if row["id"] == request_id), None)
        if item is None:
            return "Request not found", 404
        return render_template("request_detail.html", item=item)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
