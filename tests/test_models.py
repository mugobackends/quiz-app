import pytest
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from lib.database import Base, engine, get_db_session
from lib.models.category import Category
from lib.models.question import Question
from lib.models.answer import Answer
from lib.helpers import initialize_database, create_database_and_tables, seed_database

# Define a test database URL
TEST_DATABASE_URL = "sqlite:///:memory:" # Use in-memory database for tests

# Fixture for a clean database state for each test
@pytest.fixture(scope='function', autouse=True)
def setup_db_for_test():
    # Use the test engine
    test_engine = create_engine(TEST_DATABASE_URL)
    TestSession = sessionmaker(bind=test_engine)
    
    # Bind the Base metadata to the test engine
    Base.metadata.create_all(test_engine)
    
    # Override get_db_session for tests to use the in-memory db
    # This is a simple way; for more complex scenarios, consider dependency injection
    original_get_db_session = get_db_session.__wrapped__ # Access the original function
    
    def mock_get_db_session():
        return TestSession()
    
    # Temporarily replace the function in its module
    import lib.database
    lib.database.get_db_session = mock_get_db_session

    # Seed some data for tests
    seed_database_for_test(TestSession)

    yield # Run the test

    # Teardown: Drop tables after the test
    Base.metadata.drop_all(test_engine)
    
    # Restore original get_db_session
    lib.database.get_db_session = original_get_db_session


# Helper function to seed data using the test session
def seed_database_for_test(TestSession):
    session = TestSession()
    try:
        session.query(Answer).delete()
        session.query(Question).delete()
        session.query(Category).delete()
        session.commit()

        cat1 = Category(name="Test History")
        cat2 = Category(name="Test Science")
        session.add_all([cat1, cat2])
        session.commit()

        q1 = Question(text="Test Q1", category=cat1)
        q2 = Question(text="Test Q2", category=cat1)
        q3 = Question(text="Test Q3", category=cat2)
        session.add_all([q1, q2, q3])
        session.flush() # To get IDs for questions

        ans1 = Answer(text="A1 Correct", is_correct=True, question=q1)
        ans2 = Answer(text="A1 Wrong", is_correct=False, question=q1)
        ans3 = Answer(text="A2 Correct", is_correct=True, question=q2)
        session.add_all([ans1, ans2, ans3])
        session.commit()
    except Exception as e:
        session.rollback()
        raise e # Re-raise to fail the test if seeding fails
    finally:
        session.close()


# --- Test Category Model ---
def test_category_creation():
    session = get_db_session()
    new_cat = Category(name="New Category")
    session.add(new_cat)
    session.commit()
    assert new_cat.id is not None
    assert new_cat.name == "New Category"
    session.close()

def test_category_name_unique():
    session = get_db_session()
    # "Test History" is already seeded
    with pytest.raises(Exception): # Expect a unique constraint error
        session.add(Category(name="Test History"))
        session.commit()
    session.rollback() # Rollback the failed transaction
    session.close()

def test_category_get_all():
    categories = Category.get_all()
    assert len(categories) >= 2 # Test History, Test Science from fixture
    assert any(c.name == "Test History" for c in categories)

def test_category_find_by_id():
    cat = Category.find_by_name("Test History")
    found_cat = Category.find_by_id(cat.id)
    assert found_cat.name == "Test History"

def test_category_update():
    cat = Category.find_by_name("Test History")
    cat.update("Updated History")
    updated_cat = Category.find_by_id(cat.id)
    assert updated_cat.name == "Updated History"

def test_category_delete_cascades_questions_answers():
    cat = Category.find_by_name("Test History")
    initial_question_count = len(cat.questions)
    initial_total_questions = len(Question.get_all())
    initial_total_answers = len(Answer.get_all())

    cat.delete()
    assert Category.find_by_name("Test History") is None
    assert len(Question.get_all()) == initial_total_questions - initial_question_count
    # Verify answers are also deleted
    session = get_db_session()
    deleted_q_ids = [q.id for q in session.query(Question).filter(Question.category_id == cat.id).all()]
    deleted_answers = session.query(Answer).filter(Answer.question_id.in_(deleted_q_ids)).all()
    session.close()
    assert len(deleted_answers) == 0 # Should be 0 if cascade works

# --- Test Question Model ---
def test_question_creation():
    cat = Category.find_by_name("Test Science")
    new_q = Question.create("New Question Text", cat.id)
    assert new_q.id is not None
    assert new_q.text == "New Question Text"
    assert new_q.category_id == cat.id

def test_question_get_all():
    questions = Question.get_all()
    assert len(questions) >= 3 # From seed data

def test_question_find_by_id():
    q = Question.find_by_id(1) # Assuming ID 1 exists from seed
    assert q.text == "Test Q1"

def test_question_update():
    q = Question.find_by_id(1)
    q.update(new_text="Updated Question Text")
    updated_q = Question.find_by_id(1)
    assert updated_q.text == "Updated Question Text"

def test_question_delete_cascades_answers():
    q = Question.find_by_id(1) # Test Q1 has 2 answers from seed
    initial_answers_count = len(q.answers)
    initial_total_answers = len(Answer.get_all())

    q.delete()
    assert Question.find_by_id(1) is None
    assert len(Answer.get_all()) == initial_total_answers - initial_answers_count

def test_question_category_relationship():
    q = Question.find_by_id(1)
    assert isinstance(q.category, Category)
    assert q.category.name == "Test History"

def test_question_add_answer():
    q = Question.find_by_id(1)
    initial_answer_count = len(q.answers)
    new_ans = q.add_answer("Another Answer", False)
    assert new_ans.id is not None
    assert len(q.answers) == initial_answer_count + 1

# --- Test Answer Model ---
def test_answer_creation():
    q = Question.find_by_id(1)
    new_ans = Answer.create("Final Answer", True, q.id)
    assert new_ans.id is not None
    assert new_ans.text == "Final Answer"
    assert new_ans.is_correct is True
    assert new_ans.question_id == q.id

def test_answer_get_all():
    answers = Answer.get_all()
    assert len(answers) >= 3 # From seed data

def test_answer_find_by_id():
    ans = Answer.find_by_id(1) # Assuming ID 1 exists
    assert ans.text == "A1 Correct"

def test_answer_update():
    ans = Answer.find_by_id(1)
    ans.update(new_text="Updated Correct Answer", new_is_correct=False)
    updated_ans = Answer.find_by_id(1)
    assert updated_ans.text == "Updated Correct Answer"
    assert updated_ans.is_correct is False

def test_answer_delete():
    ans = Answer.find_by_id(1)
    ans.delete()
    assert Answer.find_by_id(1) is None

def test_answer_question_relationship():
    ans = Answer.find_by_id(1)
    assert isinstance(ans.question, Question)
    assert ans.question.text == "Test Q1"