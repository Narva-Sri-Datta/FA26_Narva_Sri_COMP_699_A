
import os
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    abort,
)

from werkzeug.security import check_password_hash

from config import Config
from database import connect, init_db, create_user, get_categories
from classifier import ProblemClassifier
from services import matching_providers


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    init_db(app.config["DATABASE"])

    model = ProblemClassifier(app.config["TRAINING_DATA"])
    app.extensions["problem_classifier"] = model

    # Return the currently logged-in user's information.
    def current_user():
        if not session.get("user_id"):
            return None

        with connect(app.config["DATABASE"]) as db:
            row = db.execute(
                """
                SELECT id, name, email, phone, role, active
                FROM users
                WHERE id = ?
                """,
                (session["user_id"],),
            ).fetchone()

            return dict(row) if row else None

    @app.context_processor
    def inject_user():
        return {"current_user": current_user()}

    # Check whether a user is logged in.
    def login_required(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not current_user():
                flash("Please log in to continue.", "error")
                return redirect(url_for("login"))

            return fn(*args, **kwargs)

        return wrapped

    # Restrict pages to selected account roles.
    def role_required(*roles):
        def decorator(fn):
            @wraps(fn)
            def wrapped(*args, **kwargs):
                user = current_user()

                if not user:
                    return redirect(url_for("login"))

                if user["role"] not in roles:
                    abort(403)

                return fn(*args, **kwargs)

            return wrapped

        return decorator

    # Return category names for user and provider forms.
    def categories(active=True):
        with connect(app.config["DATABASE"]) as db:
            query = (
                "SELECT name FROM categories"
                + (" WHERE active = 1" if active else "")
                + " ORDER BY name"
            )

            rows = db.execute(query).fetchall()

            return [row["name"] for row in rows]

    # --------------------------------------------------
    # Home page
    # --------------------------------------------------

    @app.get("/")
    def index():
        with connect(app.config["DATABASE"]) as db:
            counts = {
                "requests": db.execute(
                    "SELECT COUNT(*) FROM service_requests"
                ).fetchone()[0],

                "providers": db.execute(
                    "SELECT COUNT(*) FROM providers WHERE approved = 1"
                ).fetchone()[0],

                "categories": db.execute(
                    "SELECT COUNT(*) FROM categories WHERE active = 1"
                ).fetchone()[0],
            }

        return render_template("index.html", counts=counts)

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "user")

        if (
            not name
            or not email
            or not phone
            or len(password) < 8
            or role not in ("user", "provider")
        ):
            flash(
                "Complete all fields. Password must contain at least 8 characters.",
                "error",
            )
            return render_template("register.html"), 400

        # Validate provider information before creating the account.
        business = ""
        area = ""

        if role == "provider":
            business = request.form.get("business_name", "").strip()
            area = request.form.get("service_area", "").strip()

            if not business or not area:
                flash(
                    "Provider accounts need a business name and service area.",
                    "error",
                )
                return render_template("register.html"), 400

        try:
            uid = create_user(
                app.config["DATABASE"],
                name,
                email,
                phone,
                password,
                role,
            )
        except Exception:
            flash(
                "An account with this email may already exist.",
                "error",
            )
            return render_template("register.html"), 400

        if role == "provider":
            with connect(app.config["DATABASE"]) as db:
                db.execute(
                    """
                    INSERT INTO providers
                    (user_id, business_name, service_area, bio)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        uid,
                        business,
                        area,
                        request.form.get("bio", "").strip(),
                    ),
                )

        session.clear()
        session["user_id"] = uid

        if role == "provider":
            flash(
                "Account created. Provider accounts require administrator approval.",
                "success",
            )
            return redirect(url_for("provider_profile"))

        flash("Your account is ready.", "success")
        return redirect(url_for("dashboard"))

    # --------------------------------------------------
    # Login and logout
    # --------------------------------------------------

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with connect(app.config["DATABASE"]) as db:
            user = db.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,),
            ).fetchone()

        if (
            not user
            or not user["active"]
            or not check_password_hash(user["password_hash"], password)
        ):
            flash(
                "Email or password is incorrect, or the account is inactive.",
                "error",
            )
            return render_template("login.html"), 401

        session.clear()
        session["user_id"] = user["id"]

        if user["role"] == "admin":
            return redirect(url_for("admin_dashboard"))

        if user["role"] == "provider":
            return redirect(url_for("provider_dashboard"))

        return redirect(url_for("dashboard"))

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    # --------------------------------------------------
    # Local user profile
    # --------------------------------------------------

    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    @role_required("user")
    def user_profile():
        user = current_user()

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            phone = request.form.get("phone", "").strip()

            if not name or not phone:
                abort(400)

            with connect(app.config["DATABASE"]) as db:
                db.execute(
                    """
                    UPDATE users
                    SET name = ?, phone = ?
                    WHERE id = ?
                    """,
                    (name, phone, user["id"]),
                )

            flash("Profile updated.", "success")
            return redirect(url_for("user_profile"))

        return render_template("user_profile.html", profile=user)

    # --------------------------------------------------
    # User dashboard
    # --------------------------------------------------

    @app.get("/dashboard")
    @login_required
    def dashboard():
        user = current_user()

        if user["role"] != "user":
            if user["role"] == "provider":
                return redirect(url_for("provider_dashboard"))

            return redirect(url_for("admin_dashboard"))

        with connect(app.config["DATABASE"]) as db:
            rows = [
                dict(row)
                for row in db.execute(
                    """
                    SELECT *
                    FROM service_requests
                    WHERE user_id = ?
                    ORDER BY id DESC
                    """,
                    (user["id"],),
                ).fetchall()
            ]

        return render_template("dashboard.html", items=rows)

    # --------------------------------------------------
    # Create a service request
    # --------------------------------------------------

    @app.route("/requests/new", methods=["GET", "POST"])
    @login_required
    @role_required("user")
    def new_request():
        available_categories = categories()

        if request.method == "GET":
            return render_template(
                "new_request.html",
                categories=available_categories,
            )

        description = request.form.get("description", "").strip()
        chosen = request.form.get("category", "").strip()
        item = request.form.get("item_details", "").strip()
        area = request.form.get("service_area", "").strip()

        if (
            len(description) < 8
            or len(description) > 1000
            or (chosen and chosen not in available_categories)
        ):
            flash(
                "Enter a problem description between 8 and 1,000 characters and choose a valid category.",
                "error",
            )

            return render_template(
                "new_request.html",
                categories=available_categories,
                description=description,
            ), 400

        predicted, confidence = model.predict(description)
        final = chosen or predicted

        with connect(app.config["DATABASE"]) as db:
            cursor = db.execute(
                """
                INSERT INTO service_requests
                (
                    user_id,
                    description,
                    item_details,
                    service_area,
                    predicted_category,
                    final_category,
                    confidence
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    current_user()["id"],
                    description,
                    item,
                    area,
                    predicted,
                    final,
                    confidence,
                ),
            )

            request_id = cursor.lastrowid

        flash(
            f"Request submitted. Suggested category: {predicted}.",
            "success",
        )

        return redirect(
            url_for("request_detail", request_id=request_id)
        )

    # --------------------------------------------------
    # Service request details
    # --------------------------------------------------

    @app.get("/requests/<int:request_id>")
    @login_required
    def request_detail(request_id):
        user = current_user()

        with connect(app.config["DATABASE"]) as db:
            row = db.execute(
                """
                SELECT
                    sr.*,
                    u.name AS customer,
                    p.business_name
                FROM service_requests sr
                JOIN users u ON u.id = sr.user_id
                LEFT JOIN providers p ON p.user_id = sr.provider_id
                WHERE sr.id = ?
                """,
                (request_id,),
            ).fetchone()

            if not row:
                abort(404)

            if user["role"] == "user" and row["user_id"] != user["id"]:
                abort(403)

            if user["role"] == "provider" and row["provider_id"] != user["id"]:
                abort(403)

            feedback = db.execute(
                "SELECT * FROM feedback WHERE request_id = ?",
                (request_id,),
            ).fetchone()

        matches = []

        if user["role"] == "user" and not row["provider_id"]:
            matches = matching_providers(
                app.config["DATABASE"],
                row["final_category"],
                row["service_area"],
            )

        return render_template(
            "request_detail.html",
            item=dict(row),
            matches=matches,
            feedback=dict(feedback) if feedback else None,
        )

    # --------------------------------------------------
    # Change selected service category
    # --------------------------------------------------

    @app.post("/requests/<int:request_id>/category")
    @login_required
    @role_required("user")
    def change_category(request_id):
        category = request.form.get("category", "")

        if category not in categories():
            abort(400)

        with connect(app.config["DATABASE"]) as db:
            cursor = db.execute(
                """
                UPDATE service_requests
                SET final_category = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND user_id = ?
                  AND status = 'Submitted'
                """,
                (
                    category,
                    request_id,
                    current_user()["id"],
                ),
            )

            if cursor.rowcount == 0:
                abort(404)

        flash("Service category updated.", "success")

        return redirect(
            url_for("request_detail", request_id=request_id)
        )

    # --------------------------------------------------
    # Send request to a provider
    # --------------------------------------------------

    @app.post("/requests/<int:request_id>/send/<int:provider_id>")
    @login_required
    @role_required("user")
    def send_request(request_id, provider_id):
        with connect(app.config["DATABASE"]) as db:
            valid = db.execute(
                """
                SELECT 1
                FROM provider_categories pc
                JOIN categories c ON c.id = pc.category_id
                JOIN providers p ON p.user_id = pc.provider_id
                WHERE pc.provider_id = ?
                  AND c.name = (
                      SELECT final_category
                      FROM service_requests
                      WHERE id = ? AND user_id = ?
                  )
                  AND p.approved = 1
                  AND p.availability = 'Available'
                """,
                (
                    provider_id,
                    request_id,
                    current_user()["id"],
                ),
            ).fetchone()

            if not valid:
                abort(400)

            cursor = db.execute(
                """
                UPDATE service_requests
                SET provider_id = ?,
                    status = 'Sent to Provider',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND user_id = ?
                  AND provider_id IS NULL
                  AND status = 'Submitted'
                """,
                (
                    provider_id,
                    request_id,
                    current_user()["id"],
                ),
            )

            if not cursor.rowcount:
                abort(400)

        flash("Request sent to the selected provider.", "success")

        return redirect(
            url_for("request_detail", request_id=request_id)
        )

    # --------------------------------------------------
    # Cancel service request
    # --------------------------------------------------

    @app.post("/requests/<int:request_id>/cancel")
    @login_required
    @role_required("user")
    def cancel_request(request_id):
        with connect(app.config["DATABASE"]) as db:
            cursor = db.execute(
                """
                UPDATE service_requests
                SET status = 'Cancelled',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND user_id = ?
                  AND status IN (
                      'Submitted',
                      'Sent to Provider',
                      'Accepted'
                  )
                """,
                (
                    request_id,
                    current_user()["id"],
                ),
            )

            if not cursor.rowcount:
                abort(400)

        flash("Request cancelled.", "success")
        return redirect(url_for("dashboard"))

    # --------------------------------------------------
    # Provider profile
    # --------------------------------------------------

    @app.get("/providers/profile")
    @login_required
    @role_required("provider")
    def provider_profile():
        with connect(app.config["DATABASE"]) as db:
            provider = db.execute(
                """
                SELECT *
                FROM providers
                WHERE user_id = ?
                """,
                (current_user()["id"],),
            ).fetchone()

            selected = [
                row[0]
                for row in db.execute(
                    """
                    SELECT c.name
                    FROM categories c
                    JOIN provider_categories pc
                        ON pc.category_id = c.id
                    WHERE pc.provider_id = ?
                    """,
                    (current_user()["id"],),
                ).fetchall()
            ]

        return render_template(
            "provider_profile.html",
            profile=dict(provider) if provider else None,
            categories=categories(),
            selected=selected,
        )

    @app.post("/providers/profile")
    @login_required
    @role_required("provider")
    def update_provider_profile():
        name = request.form.get("business_name", "").strip()
        area = request.form.get("service_area", "").strip()
        selected = request.form.getlist("categories")
        availability = request.form.get("availability", "Available")

        available_categories = categories()

        if (
            not name
            or not area
            or availability not in ("Available", "Unavailable")
            or any(category not in available_categories for category in selected)
        ):
            abort(400)

        user_id = current_user()["id"]

        with connect(app.config["DATABASE"]) as db:
            db.execute(
                """
                UPDATE providers
                SET business_name = ?,
                    service_area = ?,
                    bio = ?,
                    availability = ?
                WHERE user_id = ?
                """,
                (
                    name,
                    area,
                    request.form.get("bio", "").strip(),
                    availability,
                    user_id,
                ),
            )

            db.execute(
                """
                DELETE FROM provider_categories
                WHERE provider_id = ?
                """,
                (user_id,),
            )

            for category in selected:
                db.execute(
                    """
                    INSERT INTO provider_categories
                    (provider_id, category_id)
                    SELECT ?, id
                    FROM categories
                    WHERE name = ?
                    """,
                    (user_id, category),
                )

        flash("Provider profile updated.", "success")
        return redirect(url_for("provider_profile"))

    # --------------------------------------------------
    # Provider dashboard
    # --------------------------------------------------

    @app.get("/provider/requests")
    @login_required
    @role_required("provider")
    def provider_dashboard():
        user_id = current_user()["id"]

        with connect(app.config["DATABASE"]) as db:
            rows = [
                dict(row)
                for row in db.execute(
                    """
                    SELECT
                        sr.*,
                        u.name AS customer,
                        u.phone
                    FROM service_requests sr
                    JOIN users u ON u.id = sr.user_id
                    WHERE sr.provider_id = ?
                       OR (
                           sr.provider_id IS NULL
                           AND sr.final_category IN (
                               SELECT c.name
                               FROM categories c
                               JOIN provider_categories pc
                                   ON pc.category_id = c.id
                               WHERE pc.provider_id = ?
                           )
                       )
                    ORDER BY sr.id DESC
                    """,
                    (user_id, user_id),
                ).fetchall()
            ]

            provider = db.execute(
                """
                SELECT approved
                FROM providers
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

        return render_template(
            "provider_dashboard.html",
            items=rows,
            approved=bool(provider and provider["approved"]),
        )

    # --------------------------------------------------
    # Provider accepts or rejects a request
    # --------------------------------------------------

    @app.post("/provider/requests/<int:request_id>/decision")
    @login_required
    @role_required("provider")
    def provider_decision(request_id):
        action = request.form.get("action")
        user_id = current_user()["id"]

        with connect(app.config["DATABASE"]) as db:
            if action == "accept":
                cursor = db.execute(
                    """
                    UPDATE service_requests
                    SET provider_id = ?,
                        status = 'Accepted',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                      AND (provider_id = ? OR provider_id IS NULL)
                      AND status IN ('Submitted', 'Sent to Provider')
                      AND EXISTS (
                          SELECT 1
                          FROM providers
                          WHERE user_id = ? AND approved = 1
                      )
                    """,
                    (
                        user_id,
                        request_id,
                        user_id,
                        user_id,
                    ),
                )

            elif action == "reject":
                cursor = db.execute(
                    """
                    UPDATE service_requests
                    SET status = 'Rejected',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                      AND provider_id = ?
                      AND status IN ('Sent to Provider', 'Accepted')
                    """,
                    (request_id, user_id),
                )

            else:
                abort(400)

            if not cursor.rowcount:
                abort(400)

        flash("Request updated.", "success")
        return redirect(url_for("provider_dashboard"))

    # --------------------------------------------------
    # Provider updates service status
    # --------------------------------------------------

    @app.post("/provider/requests/<int:request_id>/status")
    @login_required
    @role_required("provider")
    def provider_status(request_id):
        status = request.form.get("status")
        notes = request.form.get("provider_notes", "").strip()

        if status not in ("In Progress", "Completed"):
            abort(400)

        with connect(app.config["DATABASE"]) as db:
            cursor = db.execute(
                """
                UPDATE service_requests
                SET status = ?,
                    provider_notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND provider_id = ?
                  AND status IN ('Accepted', 'In Progress')
                """,
                (
                    status,
                    notes,
                    request_id,
                    current_user()["id"],
                ),
            )

            if not cursor.rowcount:
                abort(400)

        flash("Service status updated.", "success")
        return redirect(url_for("provider_dashboard"))

    # --------------------------------------------------
    # User submits feedback
    # --------------------------------------------------

    @app.post("/requests/<int:request_id>/feedback")
    @login_required
    @role_required("user")
    def add_feedback(request_id):
        try:
            rating = int(request.form.get("rating", "0"))
        except (ValueError, TypeError):
            rating = 0

        comment = request.form.get("comment", "").strip()

        with connect(app.config["DATABASE"]) as db:
            valid = db.execute(
                """
                SELECT 1
                FROM service_requests
                WHERE id = ?
                  AND user_id = ?
                  AND status = 'Completed'
                """,
                (
                    request_id,
                    current_user()["id"],
                ),
            ).fetchone()

            if not valid or rating not in range(1, 6):
                abort(400)

            db.execute(
                """
                INSERT INTO feedback
                (request_id, user_id, rating, comment)
                VALUES (?, ?, ?, ?)
                """,
                (
                    request_id,
                    current_user()["id"],
                    rating,
                    comment,
                ),
            )

        flash("Thank you for your feedback.", "success")

        return redirect(
            url_for("request_detail", request_id=request_id)
        )

    # --------------------------------------------------
    # Administrator dashboard
    # --------------------------------------------------

    @app.get("/admin")
    @login_required
    @role_required("admin")
    def admin_dashboard():
        with connect(app.config["DATABASE"]) as db:
            users = [
                dict(row)
                for row in db.execute(
                    """
                    SELECT id, name, email, role, active
                    FROM users
                    ORDER BY id DESC
                    """
                ).fetchall()
            ]

            providers = [
                dict(row)
                for row in db.execute(
                    """
                    SELECT
                        u.id,
                        u.name,
                        u.email,
                        p.business_name,
                        p.service_area,
                        p.approved
                    FROM providers p
                    JOIN users u ON u.id = p.user_id
                    ORDER BY u.id DESC
                    """
                ).fetchall()
            ]

            requests = [
                dict(row)
                for row in db.execute(
                    """
                    SELECT
                        sr.*,
                        u.name AS customer
                    FROM service_requests sr
                    JOIN users u ON u.id = sr.user_id
                    ORDER BY sr.id DESC
                    """
                ).fetchall()
            ]

        # Return category database records, not category-name strings.
        category_records = get_categories(
            app.config["DATABASE"],
            active_only=False,
        )

        return render_template(
            "admin.html",
            users=users,
            providers=providers,
            requests=requests,
            categories=category_records,
        )

    # --------------------------------------------------
    # Administrator manages user accounts
    # --------------------------------------------------

    @app.post("/admin/users/<int:user_id>/active")
    @login_required
    @role_required("admin")
    def admin_user_active(user_id):
        active = 1 if request.form.get("active") == "1" else 0

        with connect(app.config["DATABASE"]) as db:
            db.execute(
                """
                UPDATE users
                SET active = ?
                WHERE id = ? AND role != 'admin'
                """,
                (active, user_id),
            )

        return redirect(url_for("admin_dashboard"))

    # --------------------------------------------------
    # Administrator approves providers
    # --------------------------------------------------

    @app.post("/admin/providers/<int:user_id>/approval")
    @login_required
    @role_required("admin")
    def admin_provider_approval(user_id):
        approved = 1 if request.form.get("approved") == "1" else 0

        with connect(app.config["DATABASE"]) as db:
            db.execute(
                """
                UPDATE providers
                SET approved = ?
                WHERE user_id = ?
                """,
                (approved, user_id),
            )

        return redirect(url_for("admin_dashboard"))

    # --------------------------------------------------
    # Administrator adds a category
    # --------------------------------------------------

    @app.post("/admin/categories")
    @login_required
    @role_required("admin")
    def admin_add_category():
        name = request.form.get("name", "").strip()

        if not name or len(name) > 60:
            abort(400)

        with connect(app.config["DATABASE"]) as db:
            db.execute(
                """
                INSERT OR IGNORE INTO categories(name)
                VALUES (?)
                """,
                (name,),
            )

        return redirect(url_for("admin_dashboard"))

    # --------------------------------------------------
    # Administrator renames a category
    # --------------------------------------------------

    @app.post("/admin/categories/<int:category_id>/update")
    @login_required
    @role_required("admin")
    def admin_category_update(category_id):
        name = request.form.get("name", "").strip()

        if not name or len(name) > 60:
            abort(400)

        with connect(app.config["DATABASE"]) as db:
            cursor = db.execute(
                """
                UPDATE categories
                SET name = ?
                WHERE id = ?
                """,
                (name, category_id),
            )

            if not cursor.rowcount:
                abort(404)

        return redirect(url_for("admin_dashboard"))

    # --------------------------------------------------
    # Administrator removes or deactivates a category
    # --------------------------------------------------

    @app.post("/admin/categories/<int:category_id>/delete")
    @login_required
    @role_required("admin")
    def admin_category_delete(category_id):
        with connect(app.config["DATABASE"]) as db:
            category = db.execute(
                """
                SELECT id
                FROM categories
                WHERE id = ?
                """,
                (category_id,),
            ).fetchone()

            if not category:
                abort(404)

            used = db.execute(
                """
                SELECT 1
                FROM provider_categories
                WHERE category_id = ?
                LIMIT 1
                """,
                (category_id,),
            ).fetchone()

            if used:
                db.execute(
                    """
                    UPDATE categories
                    SET active = 0
                    WHERE id = ?
                    """,
                    (category_id,),
                )
            else:
                db.execute(
                    """
                    DELETE FROM categories
                    WHERE id = ?
                    """,
                    (category_id,),
                )

        return redirect(url_for("admin_dashboard"))

    # --------------------------------------------------
    # Administrator removes a service request
    # --------------------------------------------------

    @app.post("/admin/requests/<int:request_id>/remove")
    @login_required
    @role_required("admin")
    def admin_remove_request(request_id):
        with connect(app.config["DATABASE"]) as db:
            db.execute(
                """
                DELETE FROM service_requests
                WHERE id = ?
                """,
                (request_id,),
            )

        return redirect(url_for("admin_dashboard"))

    # --------------------------------------------------
    # Administrator activates or deactivates a category
    # --------------------------------------------------

    @app.post("/admin/categories/<int:category_id>/active")
    @login_required
    @role_required("admin")
    def admin_category_active(category_id):
        active = 1 if request.form.get("active") == "1" else 0

        with connect(app.config["DATABASE"]) as db:
            cursor = db.execute(
                """
                UPDATE categories
                SET active = ?
                WHERE id = ?
                """,
                (active, category_id),
            )

            if not cursor.rowcount:
                abort(404)

        return redirect(url_for("admin_dashboard"))

    # --------------------------------------------------
    # Error pages
    # --------------------------------------------------

    @app.errorhandler(403)
    def forbidden(error):
        return render_template(
            "message.html",
            title="Access denied",
            message="You do not have permission to view this page.",
        ), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template(
            "message.html",
            title="Not found",
            message="The requested record could not be found.",
        ), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
