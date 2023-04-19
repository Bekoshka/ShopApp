from core import app
from db_session import global_init
from handler import user


def main():
    global_init('data/db.sqlite')

    app.run()


if __name__ == '__main__':
    main()


# TODO
# order status
# pass in hash
