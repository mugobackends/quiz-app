import os
from lib.database import Base, engine, get_db_session
from lib.models.category import Category
from lib.models.question import Question
from lib.models.answer import Answer

def create_database_and_tables():
    """Creates the database file and all tables defined by SQLAlchemy Base."""
    # Ensure the instance directory exists
    instance_dir = os.path.join(os.getcwd(), 'instance')
    os.makedirs(instance_dir, exist_ok=True)

    Base.metadata.create_all(engine)
    print("Database tables created/ensured.")

def seed_database():
    """Seeds the database with initial categories, questions, and answers."""
    session = get_db_session()
    try:
        # Clear existing data for idempotency in seeding
        session.query(Answer).delete()
        session.query(Question).delete()
        session.query(Category).delete()
        session.commit()

        print("Seeding database...")

        # Categories
        cat_history = Category(name="History")
        cat_science = Category(name="Science")
        cat_math = Category(name="Mathematics")
        session.add_all([cat_history, cat_science, cat_math])
        session.commit() # Commit to get IDs for categories

        # Questions and Answers for History
        q1_history = Question(text="Who was the first president of the United States?", category=cat_history)
        session.add(q1_history)
        session.flush() # Flush to get question ID before adding answers
        session.add_all([
            Answer(text="Thomas Jefferson", is_correct=False, question=q1_history),
            Answer(text="George Washington", is_correct=True, question=q1_history),
            Answer(text="Abraham Lincoln", is_correct=False, question=q1_history),
            Answer(text="John Adams", is_correct=False, question=q1_history)
        ])

        q2_history = Question(text="When did World War II end?", category=cat_history)
        session.add(q2_history)
        session.flush()
        session.add_all([
            Answer(text="1942", is_correct=False, question=q2_history),
            Answer(text="1945", is_correct=True, question=q2_history),
            Answer(text="1950", is_correct=False, question=q2_history)
        ])

        # Questions and Answers for Science
        q1_science = Question(text="What is the chemical symbol for water?", category=cat_science)
        session.add(q1_science)
        session.flush()
        session.add_all([
            Answer(text="O2", is_correct=False, question=q1_science),
            Answer(text="H2O", is_correct=True, question=q1_science),
            Answer(text="CO2", is_correct=False, question=q1_science)
        ])

        q2_science = Question(text="What planet is known as the Red Planet?", category=cat_science)
        session.add(q2_science)
        session.flush()
        session.add_all([
            Answer(text="Jupiter", is_correct=False, question=q2_science),
            Answer(text="Mars", is_correct=True, question=q2_science),
            Answer(text="Venus", is_correct=False, question=q2_science)
        ])
        
        # Questions and Answers for Math
        q1_math = Question(text="What is 7 times 8?", category=cat_math)
        session.add(q1_math)
        session.flush()
        session.add_all([
            Answer(text="54", is_correct=False, question=q1_math),
            Answer(text="56", is_correct=True, question=q1_math),
            Answer(text="63", is_correct=False, question=q1_math)
        ])

        session.commit()
        print("Database seeded with sample data.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

def initialize_database():
    """Creates tables and seeds the database."""
    print("Initializing database...")
    create_database_and_tables()
    seed_database()
    print("Database initialization complete.")