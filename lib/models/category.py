from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base, get_db_session

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Define relationship to Question
    questions = relationship("Question", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

    @classmethod
    def create(cls, name):
        """Creates a new category."""
        session = get_db_session()
        try:
            new_category = cls(name=name)
            session.add(new_category)
            session.commit()
            return new_category
        except Exception as e:
            session.rollback()
            print(f"Error creating category: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def get_all(cls):
        """Returns all categories."""
        session = get_db_session()
        categories = session.query(cls).all()
        session.close()
        return categories

    @classmethod
    def find_by_id(cls, category_id):
        """Finds a category by its ID."""
        session = get_db_session()
        category = session.query(cls).filter_by(id=category_id).first()
        session.close()
        return category

    @classmethod
    def find_by_name(cls, name):
        """Finds a category by its name."""
        session = get_db_session()
        category = session.query(cls).filter_by(name=name).first()
        session.close()
        return category

    def update(self, new_name):
        """Updates the category's name."""
        session = get_db_session()
        try:
            self.name = new_name
            session.merge(self) # Re-attach and update
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error updating category: {e}")
            return False
        finally:
            session.close()

    def delete(self):
        """Deletes the category and its associated questions and answers."""
        session = get_db_session()
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting category: {e}")
            return False
        finally:
            session.close()