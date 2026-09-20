from app.core.database import Base, engine
from app.models.db_models import Job, Candidate
from app.models.user import User
from app.models.feedback import MatchFeedback

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
