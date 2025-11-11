import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from storage import Storage
from ui_manager import ManagerUI
from ui_employee import EmployeeUI

class LoginWindow(QWidget):
    def __init__(self, storage: Storage):
        super().__init__()
        self.storage = storage
        self.setWindowTitle("Login - To Do List App v1.0")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.password_input)
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.storage.authenticate(username, password)
        if user:
            self.close()
            if user.is_manager:
                ui = ManagerUI(self.storage, user)
            else:
                ui = EmployeeUI(self.storage, user)
            ui.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")

class SignupWindow(QWidget):
    def __init__(self, storage: Storage, is_manager: bool):
        super().__init__()
        self.storage = storage
        self.is_manager = is_manager
        self.setWindowTitle("Signup - To Do List App v1.0")
        self.setFixedSize(300, 300)
        layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        layout.addWidget(self.name_input)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.password_input)
        signup_btn = QPushButton("Signup")
        signup_btn.clicked.connect(self.signup)
        layout.addWidget(signup_btn)
        self.setLayout(layout)

    def signup(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        if not all([name, username, email, password]):
            QMessageBox.warning(self, "Error", "All fields required")
            return
        if self.storage.load_user_by_username(username):
            QMessageBox.warning(self, "Error", "Username exists")
            return
        if self.is_manager:
            user = self.storage.create_manager(name, email, username, password)
        else:
            user = self.storage.create_employee(name, email, username, password)
        QMessageBox.information(self, "Success", f"Account created. Your App ID: {user.id}\nRemember it for assignments.")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))  # Assume icon.png exists in the same directory
    storage = Storage()
    manager = storage.get_manager()
    if not manager:
        signup = SignupWindow(storage, is_manager=True)
        signup.show()
    else:
        login = LoginWindow(storage)
        login.show()
    sys.exit(app.exec())