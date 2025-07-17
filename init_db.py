from models import Base, engine

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()