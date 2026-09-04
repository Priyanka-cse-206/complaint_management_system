# complaint.py
# Complaint Form - Smart Solutions + YouTube + Submit Complaint

import sys
import webbrowser
from urllib.parse import quote_plus

import mysql.connector

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QTextEdit, QPushButton, QVBoxLayout,
    QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt, QDate


class ComplaintWindow(QWidget):

    def __init__(self, username):
        super().__init__()

        self.username = username

        self.setWindowTitle("Smart Complaint System")
        self.setFixedSize(750, 920)

        self.setStyleSheet("""
            QWidget{
                background:#f5f7fa;
                font-family:Segoe UI;
            }

            QLabel{
                font-size:14px;
                font-weight:bold;
                color:#2c3e50;
            }

            QLabel#title{
                font-size:26px;
                font-weight:bold;
            }

            QLineEdit,QTextEdit,QComboBox{
                background:white;
                border:1px solid #dcdde1;
                border-radius:8px;
                padding:10px;
                font-size:14px;
            }

            QPushButton{
                background:#3498db;
                color:white;
                border:none;
                padding:12px;
                border-radius:8px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#2980b9;
            }
        """)

        self.create_ui()

    # ---------------- UI ----------------
    def create_ui(self):

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Real Life Smart Complaint Form")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Username
        self.user_box = QLineEdit()
        self.user_box.setText(self.username)
        self.user_box.setReadOnly(True)

        # Complaint Title
        self.comp_title = QLineEdit()
        self.comp_title.setPlaceholderText("Complaint Title")

        # Category
        self.category = QComboBox()
        self.category.addItems([
            "Fan Problem",
            "Electric Issue",
            "Water Leakage",
            "Broken Chair",
            "Internet Problem",
            "Cleaning",
            "Teacher Shortage",
            "Other"
        ])

        # Priority
        self.priority = QComboBox()
        self.priority.addItems([
            "Low",
            "Medium",
            "High"
        ])

        # Location
        self.location = QLineEdit()
        self.location.setPlaceholderText("Problem Location")

        # Description
        self.description = QTextEdit()
        self.description.setPlaceholderText(
            "Write issue in detail..."
        )

        # Smart Suggestions
        self.ai_box = QTextEdit()
        self.ai_box.setReadOnly(True)

        # Date
        self.date_box = QLineEdit()
        self.date_box.setText(
            QDate.currentDate().toString("dd-MM-yyyy")
        )
        self.date_box.setReadOnly(True)

        # ---------------- BUTTONS ----------------

        suggest_btn = QPushButton(
            "Get Smart Solutions"
        )
        suggest_btn.clicked.connect(
            self.get_solution
        )

        yt_btn = QPushButton(
            "Open Repair Videos"
        )
        yt_btn.clicked.connect(
            self.open_youtube
        )

        submit_btn = QPushButton(
            "Submit Complaint"
        )
        submit_btn.clicked.connect(
            self.save_data
        )

        # ---------------- ADD WIDGETS ----------------

        layout.addWidget(title)

        layout.addWidget(
            QLabel("Username")
        )
        layout.addWidget(
            self.user_box
        )

        layout.addWidget(
            QLabel("Complaint Title")
        )
        layout.addWidget(
            self.comp_title
        )

        layout.addWidget(
            QLabel("Category")
        )
        layout.addWidget(
            self.category
        )

        layout.addWidget(
            QLabel("Priority")
        )
        layout.addWidget(
            self.priority
        )

        layout.addWidget(
            QLabel("Problem Location")
        )
        layout.addWidget(
            self.location
        )

        layout.addWidget(
            QLabel("Description")
        )
        layout.addWidget(
            self.description
        )

        layout.addWidget(
            suggest_btn
        )

        layout.addWidget(
            yt_btn
        )

        layout.addWidget(
            QLabel("Smart Suggestions")
        )

        layout.addWidget(
            self.ai_box
        )

        layout.addWidget(
            QLabel("Date")
        )

        layout.addWidget(
            self.date_box
        )

        layout.addWidget(
            submit_btn
        )

        self.setLayout(layout)

    # ---------------- SMART SOLUTIONS ----------------
    def get_solution(self):

        QMessageBox.information(
            self,
            "Clicked",
            "Button Working"
        )

        issue = self.category.currentText().lower()
        loc = self.location.text()

        if "fan" in issue:

            result = f"""
Problem: Fan Not Working

Nearby Electricians:
1. Raj Electrician - 9876543210
2. Sharma Repair - 9123456780

Solutions:
1. Check switch board
2. Check regulator
3. Replace capacitor
4. Check motor

Location:
{loc}
"""

        elif "water" in issue:

            result = f"""
Problem: Water Leakage

Nearby Plumbers:
1. Mohan Plumber - 9988776655
2. Gupta Plumbing - 9871234567

Solutions:
1. Close valve
2. Check pipe
3. Seal leakage
4. Replace pipe

Location:
{loc}
"""

        elif "chair" in issue:

            result = f"""
Problem: Broken Chair

Nearby Carpenter:
1. Ravi Carpenter - 9012121212
2. Wood Fixer - 9089898989

Solutions:
1. Tighten screws
2. Repair leg
3. Replace seat
4. Temporary support

Location:
{loc}
"""

        elif "teacher" in issue:

            result = f"""
Problem: Teacher Shortage

Solutions:
1. Temporary teacher hiring
2. Online classes
3. Guest faculty
4. New recruitment

Location:
{loc}
"""

        else:

            result = f"""
General Issue

Solutions:
1. Inspect issue
2. Send worker
3. Mark urgent
4. Admin review

Location:
{loc}
"""

        self.ai_box.clear()
        self.ai_box.setPlainText(
            result
        )

    # ---------------- YOUTUBE ----------------
    def open_youtube(self):

        issue = self.category.currentText()

        query = issue + " repair"

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )

        webbrowser.open(url)

    # ---------------- DATABASE ----------------
    def connect_db(self):

        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Priyanka@123",
            database="complaint_system"
        )

    # ---------------- SAVE DATA ----------------
    def save_data(self):

        try:

            conn = self.connect_db()
            cursor = conn.cursor()

            query = """
                INSERT INTO complaints
                (
                    username,
                    title,
                    category,
                    priority,
                    location,
                    description,
                    ai_suggestion,
                    status
                )
                VALUES
                (
                    %s,%s,%s,%s,
                    %s,%s,%s,%s
                )
            """

            values = (
                self.user_box.text(),
                self.comp_title.text(),
                self.category.currentText(),
                self.priority.currentText(),
                self.location.text(),
                self.description.toPlainText(),
                self.ai_box.toPlainText(),
                "Pending"
            )

            cursor.execute(
                query,
                values
            )

            conn.commit()
            conn.close()

            QMessageBox.information(
                self,
                "Success",
                "Complaint Submitted to Admin"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                str(e)
            )


# ---------------- RUN ----------------
if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = ComplaintWindow("Saurav")
    win.show()

    sys.exit(app.exec_())