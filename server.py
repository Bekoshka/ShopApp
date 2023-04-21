from core import app
from db_session import global_init
from handler.auth import init_admin


def main():
    global_init('data/db.sqlite')
    init_admin()
    app.run()


if __name__ == '__main__':
    main()
