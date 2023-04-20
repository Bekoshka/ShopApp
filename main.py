from core import app
from db_session import global_init


def main():
    global_init('data/db.sqlite')

    app.run()


if __name__ == '__main__':
    main()


# TODO
# pass in hash
# reduce remainder
# add error info to all pages
# status in rus