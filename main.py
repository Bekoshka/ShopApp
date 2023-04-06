from core import app
from db_session import global_init
from handler import user
from handler import test


def main():
    global_init('data/db.sqlite')
    app.run()


if __name__ == '__main__':
    main()