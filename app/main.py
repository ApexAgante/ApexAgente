import tkinter as tk
from gui.login.gui import login_window

root = tk.Tk()
root.withdraw()

if __name__ == "__main__":
    login_window(root)
    root.mainloop()
