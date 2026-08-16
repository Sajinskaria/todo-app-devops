import os
import logging

from flask import Flask, render_template, request, redirect, url_for
from database import get_connection


# --------------------------------------------------
# Flask Application
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Home / View Todos
# --------------------------------------------------

@app.route("/")
def index():
    logger.info("Loading todo list")

    connection = get_connection()

    if connection is None:
        logger.error("Unable to load todo list: database connection failed")
        return "Database connection failed", 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM todos ORDER BY created_at DESC"
        )

        todos = cursor.fetchall()

        cursor.close()

        logger.info("Successfully loaded %d todo(s)", len(todos))

        return render_template("index.html", todos=todos)

    except Exception as error:
        logger.error("Error loading todos: %s", error)
        return "Error loading tasks", 500

    finally:
        connection.close()


# --------------------------------------------------
# Add Todo
# --------------------------------------------------

@app.route("/add", methods=["POST"])
def add_todo():

    title = request.form.get("title", "").strip()

    logger.info("Add todo request received")

    if not title:
        logger.warning("Empty todo title submitted")
        return redirect(url_for("index"))

    connection = get_connection()

    if connection is None:
        logger.error("Unable to add todo: database connection failed")
        return "Database connection failed", 500

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO todos (title) VALUES (%s)",
            (title,)
        )

        connection.commit()

        logger.info("Todo added successfully")

        cursor.close()

        return redirect(url_for("index"))

    except Exception as error:
        connection.rollback()

        logger.error("Error adding todo: %s", error)

        return "Error adding task", 500

    finally:
        connection.close()


# --------------------------------------------------
# Complete / Undo Todo
# --------------------------------------------------

@app.route("/complete/<int:todo_id>")
def complete_todo(todo_id):

    logger.info("Updating todo id=%s", todo_id)

    connection = get_connection()

    if connection is None:
        logger.error(
            "Unable to update todo id=%s: database connection failed",
            todo_id
        )
        return "Database connection failed", 500

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE todos
            SET completed = NOT completed
            WHERE id = %s
            """,
            (todo_id,)
        )

        connection.commit()

        logger.info("Todo id=%s updated successfully", todo_id)

        cursor.close()

        return redirect(url_for("index"))

    except Exception as error:
        connection.rollback()

        logger.error(
            "Error updating todo id=%s: %s",
            todo_id,
            error
        )

        return "Error updating task", 500

    finally:
        connection.close()


# --------------------------------------------------
# Delete Todo
# --------------------------------------------------

@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):

    logger.info("Deleting todo id=%s", todo_id)

    connection = get_connection()

    if connection is None:
        logger.error(
            "Unable to delete todo id=%s: database connection failed",
            todo_id
        )
        return "Database connection failed", 500

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM todos WHERE id = %s",
            (todo_id,)
        )

        connection.commit()

        logger.info("Todo id=%s deleted successfully", todo_id)

        cursor.close()

        return redirect(url_for("index"))

    except Exception as error:
        connection.rollback()

        logger.error(
            "Error deleting todo id=%s: %s",
            todo_id,
            error
        )

        return "Error deleting task", 500

    finally:
        connection.close()


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/health")
def health():

    connection = get_connection()

    if connection is None:

        logger.error(
            "Health check failed: database unavailable"
        )

        return {
            "status": "unhealthy"
        }, 503

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT 1")

        cursor.fetchone()

        cursor.close()

        logger.info("Health check successful")

        return {
            "status": "healthy"
        }, 200

    except Exception as error:

        logger.error(
            "Health check failed: %s",
            error
        )

        return {
            "status": "unhealthy"
        }, 503

    finally:
        connection.close()


# --------------------------------------------------
# Application Entry Point
# --------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.getenv("PORT", "5000")
    )

    logger.info(
        "Starting To-Do application on port %s",
        port
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
