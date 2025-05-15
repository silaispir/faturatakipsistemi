import sys
from PyQt5.QtWidgets import QApplication
from database.database import Database
from windows.login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Database()
    login_window = LoginWindow(db)
    login_window.show()
    sys.exit(app.exec_())