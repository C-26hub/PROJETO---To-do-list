from data_handler import *
from db_functions import *
from user_interface import *

def main():
    try:
        pass
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            create_db()

if __name__ == "__main__":
    main()
