import os
import time
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@db:5432/todos",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


@app.route("/")
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template("index.html", todos=todos)


@app.route("/todos", methods=["POST"])
def add_todo():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if title:
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()

    return redirect(url_for("index"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


def initialize_database(max_attempts: int = 30, delay_seconds: int = 2) -> None:
    with app.app_context():
        for attempt in range(1, max_attempts + 1):
            try:
                db.create_all()
                app.logger.info("Database connection established.")
                return
            except OperationalError as exc:
                db.session.remove()

                if attempt == max_attempts:
                    app.logger.error(
                        "Database was not ready after %s attempts.",
                        max_attempts,
                    )
                    raise

                app.logger.warning(
                    "Database unavailable. Retrying in %s seconds "
                    "(attempt %s/%s): %s",
                    delay_seconds,
                    attempt,
                    max_attempts,
                    exc,
                )
                time.sleep(delay_seconds)


initialize_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
