from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from lib.database import Base, get_db_session
from lib.models.question import Question # Import Question

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)

    # Define relationship to Question
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer(id={self.id}, text='{self.text[:30]}...', correct={self.is_correct}, question_id={self.question_id})>"

    @classmethod
    def create(cls, text, is_correct, question_id):
        """Creates a new answer."""
        session = get_db_session()
        try:
            # Optional: Check if question_id exists
            if not Question.find_by_id(question_id):
                raise ValueError(f"Question with ID {question_id} does not exist.")

            new_answer = cls(text=text, is_correct=is_correct, question_id=question_id)
            session.add(new_answer)
            session.commit()
            return new_answer
        except Exception as e:
            session.rollback()
            print(f"Error creating answer: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def get_all(cls):
        """Returns all answers."""
        session = get_db_session()
        answers = session.query(cls).all()
        session.close()
        return answers

    @classmethod
    def find_by_id(cls, answer_id):
        """Finds an answer by its ID."""
        session = get_db_session()
        answer = session.query(cls).filter_by(id=answer_id).first()
        session.close()
        return answer

    def update(self, new_text=None, new_is_correct=None):
        """Updates the answer's text or correctness."""
        session = get_db_session()
        try:
            if new_text:
                self.text = new_text
            if new_is_correct is not None: # Can be False
                self.is_correct = new_is_correct
            session.merge(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error updating answer: {e}")
            return False
        finally:
            session.close()

    def delete(self):
        """Deletes the answer."""
        session = get_db_session()
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting answer: {e}")
            return False
        finally:
            session.close()