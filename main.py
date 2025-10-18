from app.windows.login_window import main
from app.database.session import Base, engine

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    main()
