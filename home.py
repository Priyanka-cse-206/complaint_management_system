# home.py
# Dynamic Dashboard with MySQL Live Counts

import sys
import mysql.connector

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QGridLayout,
    QMessageBox
)
from PyQt5.QtCore import Qt


class HomeWindow(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username

        self.setWindowTitle("Complaint Management Dashboard")
        self.setFixedSize(1100, 700)

        self.setStyleSheet("""
            QWidget{
                background:#f5f7fa;
                font-family:Segoe UI;
            }

            QFrame#sidebar{
                background:#1e2a38;
                border-radius:15px;
            }

            QLabel#logo{
                color:white;
                font-size:24px;
                font-weight:bold;
            }

            QLabel#user{
                color:#dfe6e9;
                font-size:15px;
            }

            QPushButton#menu{
                background:#34495e;
                color:white;
                padding:12px;
                border:none;
                border-radius:10px;
                text-align:left;
                font-size:14px;
            }

            QPushButton#menu:hover{
                background:#3498db;
            }

            QPushButton#logout{
                background:#e74c3c;
                color:white;
                padding:12px;
                border:none;
                border-radius:10px;
                font-size:14px;
            }

            QPushButton#logout:hover{
                background:#c0392b;
            }

            QLabel#title{
                font-size:28px;
                font-weight:bold;
                color:#2c3e50;
            }

            QFrame#card{
                background:white;
                border-radius:15px;
                border:1px solid #dcdde1;
            }

            QLabel#cardTitle{
                font-size:18px;
                font-weight:bold;
                color:#2c3e50;
            }

            QLabel#number{
                font-size:34px;
                font-weight:bold;
                color:#3498db;
            }

            QPushButton#action{
                background:#2ecc71;
                color:white;
                padding:10px;
                border:none;
                border-radius:8px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton#action:hover{
                background:#27ae60;
            }
        """)

        self.create_ui()
        self.load_counts()

    # ---------------- DATABASE ----------------
    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Priyanka@123",
            database="complaint_system"
        )

    # ---------------- UI ----------------
    def create_ui(self):
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)

        side_layout = QVBoxLayout()
        side_layout.setContentsMargins(20, 20, 20, 20)
        side_layout.setSpacing(15)

        logo = QLabel("🛠 CMS")
        logo.setObjectName("logo")

        user = QLabel(f"Welcome, {self.username}")
        user.setObjectName("user")

        btn1 = QPushButton("📌 Submit Complaint")
        btn1.setObjectName("menu")
        btn1.clicked.connect(self.submit_complaint)

        btn2 = QPushButton("📊 My Complaints")
        btn2.setObjectName("menu")
        btn2.clicked.connect(self.my_complaints)

        btn3 = QPushButton("🔄 Refresh Dashboard")
        btn3.setObjectName("menu")
        btn3.clicked.connect(self.load_counts)

        logout = QPushButton("Logout")
        logout.setObjectName("logout")
        logout.clicked.connect(self.logout)

        side_layout.addWidget(logo)
        side_layout.addWidget(user)
        side_layout.addSpacing(20)
        side_layout.addWidget(btn1)
        side_layout.addWidget(btn2)
        side_layout.addWidget(btn3)
        side_layout.addStretch()
        side_layout.addWidget(logout)

        sidebar.setLayout(side_layout)

        # Right Content
        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Dashboard")
        title.setObjectName("title")

        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        # Create labels for numbers
        self.total_label = QLabel("0")
        self.pending_label = QLabel("0")
        self.resolved_label = QLabel("0")
        self.my_label = QLabel("0")

        card1 = self.create_card("Total Complaints", self.total_label)
        card2 = self.create_card("Pending", self.pending_label)
        card3 = self.create_card("Resolved", self.resolved_label)
        card4 = self.create_card("My Complaints", self.my_label)

        self.grid.addWidget(card1, 0, 0)
        self.grid.addWidget(card2, 0, 1)
        self.grid.addWidget(card3, 1, 0)
        self.grid.addWidget(card4, 1, 1)

        quick_btn = QPushButton("➕ New Complaint")
        quick_btn.setObjectName("action")
        quick_btn.clicked.connect(self.submit_complaint)

        content.addWidget(title)
        content.addSpacing(10)
        content.addLayout(self.grid)
        content.addSpacing(20)
        content.addWidget(quick_btn)
        content.addStretch()

        main_layout.addWidget(sidebar)
        main_layout.addLayout(content)

        self.setLayout(main_layout)

    # ---------------- CARD ----------------
    def create_card(self, title_text, number_label):
        card = QFrame()
        card.setObjectName("card")
        card.setFixedSize(360, 180)

        layout = QVBoxLayout()

        title = QLabel(title_text)
        title.setObjectName("cardTitle")

        number_label.setObjectName("number")
        number_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(number_label)
        layout.addStretch()

        card.setLayout(layout)
        return card

    # ---------------- LOAD COUNTS ----------------
    def load_counts(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            # Total
            cursor.execute("SELECT COUNT(*) FROM complaints")
            total = cursor.fetchone()[0]

            # Pending
            cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
            pending = cursor.fetchone()[0]

            # Resolved
            cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
            resolved = cursor.fetchone()[0]

            # My complaints
            cursor.execute(
                "SELECT COUNT(*) FROM complaints WHERE username=%s",
                (self.username,)
            )
            my_count = cursor.fetchone()[0]

            self.total_label.setText(str(total))
            self.pending_label.setText(str(pending))
            self.resolved_label.setText(str(resolved))
            self.my_label.setText(str(my_count))

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    # ---------------- BUTTONS ----------------
    def submit_complaint(self):
        from complaint import ComplaintWindow

        self.win = ComplaintWindow(self.username)
        self.win.show()

    def my_complaints(self):
        from my_complaints import MyComplaintsWindow

        self.win = MyComplaintsWindow(self.username)
        self.win.show()

    def logout(self):
        self.close()


# ---------------- TEST ----------------
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = HomeWindow("Saurav")
    window.show()

    sys.exit(app.exec_())