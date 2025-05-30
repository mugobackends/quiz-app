from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.database import Base, get_db_session
from lib.models.category import Category # Import Category

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # Define relationships
    category = relationship("Category", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Question(id={self.id}, text='{self.text[:30]}...', category_id={self.category_id})>"

    @classmethod
    def create(cls, text, category_id):
        """Creates a new question."""
        session = get_db_session()
        try:
            # Optional: Check if category_id exists
            if not Category.find_by_id(category_id):
                raise ValueError(f"Category with ID {category_id} does not exist.")

            new_question = cls(text=text, category_id=category_id)
            session.add(new_question)
            session.commit()
            return new_question
        except Exception as e:
            session.rollback()
            print(f"Error creating question: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def get_all(cls):
        """Returns all questions."""
        session = get_db_session()
        questions = session.query(cls).all()
        session.close()
        return questions

    @classmethod
    def find_by_id(cls, question_id):
        """Finds a question by its ID."""
        session = get_db_session()
        question = session.query(cls).filter_by(id=question_id).first()
        session.close()
        return question

    def update(self, new_text=None, new_category_id=None):
        """Updates the question's text or category."""
        session = get_db_session()
        try:
            if new_text:
                self.text = new_text
            if new_category_id:
                if not Category.find_by_id(new_category_id):
                    raise ValueError(f"Category with ID {new_category_id} does not exist.")
                self.category_id = new_category_id
            session.merge(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error updating question: {e}")
            return False
        finally:
            session.close()

    def delete(self):
        """Deletes the question and its associated answers."""
        session = get_db_session()
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting question: {e}")
            return False
        finally:
            session.close()

    def add_answer(self, text, is_correct):
        """Adds an answer to this question."""
        from lib.models.answer import Answer # Import locally to avoid circular dependency
        return Answer.create(text, is_correct, self.id)