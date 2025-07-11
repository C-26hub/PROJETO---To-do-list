import db_functions as db
from user_interface import start_app

def main():
    db.create_db()
    start_app()

if __name__ == "__main__":
    main()
    
