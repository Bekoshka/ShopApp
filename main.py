from core import app
from db_session import global_init
from handler import user


def main():
    global_init('data/db.sqlite')

    app.run()


if __name__ == '__main__':
    main()


# TODO
# cart UI
# add to cart
# orders
# order details
# pass in hash
# filter by category
