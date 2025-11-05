import sys
import traceback
from app.windows.login_window import main
from app.database.session import Base, engine

# Создание всех таблиц в базе
Base.metadata.create_all(bind=engine)


def excepthook(exctype, value, tb):
    print("⚠️ Ошибка в приложении:")
    traceback.print_exception(exctype, value, tb)
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = excepthook

if __name__ == '__main__':
    main()
