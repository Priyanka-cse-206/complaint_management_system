# my_complaints.py
# Correct Full Code

import sys
import mysql.connector

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox,
    QHeaderView
)
from PyQt5.QtCore import Qt


class MyComplaintsWindow(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username

        self.setWindowTitle("My Complaints")
        self.setFixedSize(1050, 680)

        self.setStyleSheet("""
            QWidget{
                background:#f5f7fa;
                font-family:Segoe UI;
            }

            QLabel#title{
                font-size:28px;
                font-weight:bold;
                color:#2c3e50;
            }

            QLabel#user{
                font-size:14px;
                color:#7f8c8d;
            }

            QTableWidget{
                background:white;
                border-radius:10px;
                border:1px solid #dcdde1;
                gridline-color:#ecf0f1;
                font-size:13px;
            }

            QHeaderView::section{
                background:#3498db;
                color:white;
                padding:8px;
                border:none;
                font-weight:bold;
            }

            QPushButton{
                background:#3498db;
                color:white;
                border:none;
                padding:10px;
                border-radius:8px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#2980b9;
            }

            QPushButton#closebtn{
                background:#e74c3c;
            }

            QPushButton#closebtn:hover{
                background:#c0392b;
            }
        """)

        self.create_ui()
        self.load_data()

    # ---------------- UI ----------------
    def create_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("My Complaints")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        user = QLabel(f"Logged in as: {self.username}")
        user.setObjectName("user")
        user.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Title",
            "Category",
            "Priority",
            "Description",
            "Date",
            "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)

        btn_layout = QHBoxLayout()

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_data)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("closebtn")
        close_btn.clicked.connect(self.close)

        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(close_btn)

        layout.addWidget(title)
        layout.addWidget(user)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    # ---------------- DATABASE ----------------
    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Priyanka@123",
            database="complaint_system"
        )

    # ---------------- LOAD DATA ----------------
    def load_data(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            query = """
                SELECT id, title, category, priority,
                       description, date, status
                FROM complaints
                WHERE username=%s
                ORDER BY id DESC
            """

            cursor.execute(query, (self.username,))
            rows = cursor.fetchall()

            self.table.setRowCount(0)

            for row_number, row_data in enumerate(rows):
                self.table.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(
                        row_number,
                        column_number,
                        item
                    )

            conn.close()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                str(e)
            )


# ---------------- TEST ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyComplaintsWindow("Priyanka")
    window.show()

    sys.exit(app.exec_())
