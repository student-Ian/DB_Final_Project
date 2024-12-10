from login import login
from client import connect_to_server, close_connection


def main():
    connect_to_server(host='127.0.0.1', port=9876)
    login()
    close_connection()


if __name__ == "__main__":
    main()


# polypite
# 4db7920bc89a995c
