import tkinter as tk
import db_functions as db
from user_interface import AppUi

def main():
    db.create_db()
    root= tk.Tk()
    app = AppUi(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    