# Quiz App CLI + ORM Project

## Project Overview

This project is a Command Line Interface (CLI) quiz application built with Python and SQLAlchemy ORM. It allows users to take quizzes on various categories and provides basic administrative functions for managing questions and categories. The application adheres to best practices in CLI design, database interaction, and project structure.

## Real-World Problem Solved

This application provides a simple, interactive way to:
* **Test Knowledge:** Users can select a quiz category and answer questions.
* **Learn and Practice:** Immediate feedback is provided for each answer.
* **Manage Content:** Administrators can add, view, update, and delete categories and questions directly from the command line.

## Learning Goals Addressed

This project directly addresses several key learning objectives:

1.  **CLI Application:** The entire user interaction is handled through a command-line interface, demonstrating input handling, output formatting, and menu navigation.
2.  **SQLAlchemy ORM with 3+ related tables:**
    * **`Category`**: Represents a quiz topic (e.g., "History", "Science").
    * **`Question`**: Belongs to a `Category` and contains the question text.
    * **`Answer`**: Belongs to a `Question` and stores potential answers, one of which is marked as correct.
    * **Relationships:**
        * One `Category` has many `Question`s (one-to-many).
        * One `Question` has many `Answer`s (one-to-many).
        * Implicitly, `Category` indirectly relates to `Answer`s via `Question`s.
3.  **Well-maintained virtual environment using Pipenv:** The project uses `Pipenv` for dependency management, ensuring a consistent and isolated development environment. The `Pipfile` lists all project dependencies.
4.  **Proper package structure:** The code is organized into logical directories (`lib/`, `lib/models/`, `lib/db/`, `migrations/`) with appropriate `__init__.py` files, enhancing modularity and maintainability.
5.  **Use of lists, dicts, and tuples:**
    * **Lists:** Used for storing collections of objects (e.g., all questions in a category, multiple answers for a question).
    * **Dictionaries:** Used for passing keyword arguments to ORM constructors, storing question/answer data, and representing user choices.
    * **Tuples:** Can be used for immutable collections, e.g., representing choices in a menu system.

## Setup Instructions

### Prerequisites

* Python 3.7+
* `pipenv`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/quiz-app.git](https://github.com/your-username/quiz-app.git) # Replace with your repo URL
    cd quiz-app
    ```

2.  **Install dependencies and activate the virtual environment:**
    ```bash
    pipenv install
    pipenv shell
    ```

3.  **Initialize the database:**
    This will create an `instance/quiz_app.db` SQLite database file and set up all necessary tables.
    ```bash
    python main.py initdb
    ```

## How to Run

1.  **Activate the virtual environment (if not already active):**
    ```bash
    pipenv shell
    ```
2.  **Start the CLI application:**
    ```bash
    python main.py
    ```

## CLI Commands

* `python main.py`: Starts the main menu of the quiz application.
* `python main.py initdb`: Initializes or resets the database with initial schema and some seed data.
* `python main.py runtests`: Runs the pytest unit tests.

## Database Schema

The database uses SQLite and is managed by SQLAlchemy ORM. The schema includes:

* **`categories` table**:
    * `id` (Primary Key)
    * `name` (String, Unique)
* **`questions` table**:
    * `id` (Primary Key)
    * `text` (String)
    * `category_id` (Foreign Key to `categories.id`)
* **`answers` table**:
    * `id` (Primary Key)
    * `text` (String)
    * `is_correct` (Boolean)
    * `question_id` (Foreign Key to `questions.id`)

## Project Structure