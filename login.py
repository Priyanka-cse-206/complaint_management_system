# login_ui.py
# Login with Role Picklist (Admin / Student / Teacher / Others)

import sys
import mysql.connector

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox,
    QComboBox
)
from PyQt5.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Complaint Management System")
        self.setFixedSize(430, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: Arial;
            }

            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
            }

            QLabel#subtitle {
                font-size: 14px;
                color: #7f8c8d;
            }

            QLineEdit, QComboBox {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background: white;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }

            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QPushButton#register {
                background-color: #2ecc71;
            }

            QPushButton#register:hover {
                background-color: #27ae60;
            }
        """)

        self.create_ui()

    # ---------------- UI ----------------
    def create_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        title = QLabel("Login")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Complaint Management System")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.role_box = QComboBox()
        self.role_box.addItems([
            "Admin",
            "Student",
            "Teacher",
            "Others"
        ])

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)

        register_btn = QPushButton("Register")
        register_btn.setObjectName("register")
        register_btn.clicked.connect(self.register_user)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(15)
        layout.addWidget(self.role_box)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)
        layout.addStretch()

        self.setLayout(layout)

    # ---------------- DATABASE ----------------
    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Priyanka@123",
            database="complaint_system"
        )

    # ---------------- LOGIN ----------------
    def login(self):
        selected_role = self.role_box.currentText().lower()
        user = self.username.text().strip()
        pwd = self.password.text().strip()

        if user == "" or pwd == "":
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            query = """
                SELECT username, role
                FROM users
                WHERE username=%s AND password=%s
            """

            cursor.execute(query, (user, pwd))
            result = cursor.fetchone()

            if result:
                db_role = result[1].lower()

                # Role must match selected picklist
                if selected_role != db_role:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Selected role does not match account role"
                    )
                    conn.close()
                    return

                QMessageBox.information(
                    self,
                    "Success",
                    "Login Successful"
                )

                # Admin -> admin.py
                if selected_role == "admin":
                    from admin import AdminWindow
                    self.win = AdminWindow()
                    self.win.show()

                # Everyone else -> home.py
                else:
                    from home import HomeWindow
                    self.win = HomeWindow(user)
                    self.win.show()

                self.close()

            else:
                QMessageBox.warning(
                    self,
                    "Failed",
                    "Incorrect Username or Password"
                )

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ---------------- REGISTER ----------------
    def register_user(self):
        role = self.role_box.currentText().lower()
        user = self.username.text().strip()
        pwd = self.password.text().strip()

        if user == "" or pwd == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please fill username and password"
            )
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE username=%s",
                (user,)
            )

            existing = cursor.fetchone()

            if existing:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Username already exists"
                )
                conn.close()
                return

            query = """
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
            """

            cursor.execute(query, (user, pwd, role))
            conn.commit()
            conn.close()

            QMessageBox.information(
                self,
                "Success",
                "Registration Successful"
            )

            self.username.clear()
            self.password.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())