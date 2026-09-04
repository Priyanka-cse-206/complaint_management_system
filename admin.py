# admin.py
# Admin Panel - View Complaints + Update Status
# + Delete Complaint + Find Nearby Mechanic

import sys
import webbrowser
from urllib.parse import quote_plus

import mysql.connector

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem,
    QComboBox, QHeaderView
)

from PyQt5.QtCore import Qt


class AdminWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Panel")
        self.setFixedSize(1200, 700)

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

            QTableWidget{
                background:white;
                border:1px solid #dcdde1;
                border-radius:10px;
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

            QPushButton#delete{
                background:#e74c3c;
            }

            QPushButton#delete:hover{
                background:#c0392b;
            }

            QPushButton#mechanic{
                background:#9b59b6;
            }

            QPushButton#mechanic:hover{
                background:#8e44ad;
            }

            QComboBox{
                padding:8px;
                border-radius:8px;
                background:white;
            }
        """)

        self.create_ui()
        self.load_data()

    # ---------------- UI ----------------
    def create_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            20, 20, 20, 20
        )

        layout.setSpacing(15)

        title = QLabel(
            "Admin Complaint Management"
        )

        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # ---------------- TABLE ----------------

        self.table = QTableWidget()

        # 9 columns now because Location is included
        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Username",
            "Title",
            "Category",
            "Priority",
            "Location",
            "Date",
            "Status",
            "Description"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        # ---------------- BUTTONS ----------------

        btn_layout = QHBoxLayout()

        self.status_box = QComboBox()

        self.status_box.addItems([
            "Pending",
            "In Progress",
            "Resolved"
        ])

        refresh_btn = QPushButton(
            "Refresh"
        )

        refresh_btn.clicked.connect(
            self.load_data
        )

        update_btn = QPushButton(
            "Update Status"
        )

        update_btn.clicked.connect(
            self.update_status
        )

        delete_btn = QPushButton(
            "Delete Complaint"
        )

        delete_btn.setObjectName(
            "delete"
        )

        delete_btn.clicked.connect(
            self.delete_complaint
        )

        # NEW BUTTON
        mechanic_btn = QPushButton(
            "Find Nearby Mechanic"
        )

        mechanic_btn.setObjectName(
            "mechanic"
        )

        mechanic_btn.clicked.connect(
            self.find_mechanic
        )

        btn_layout.addWidget(
            self.status_box
        )

        btn_layout.addWidget(
            update_btn
        )

        btn_layout.addWidget(
            mechanic_btn
        )

        btn_layout.addWidget(
            delete_btn
        )

        btn_layout.addWidget(
            refresh_btn
        )

        layout.addWidget(title)

        layout.addWidget(
            self.table
        )

        layout.addLayout(
            btn_layout
        )

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
                SELECT
                    id,
                    username,
                    title,
                    category,
                    priority,
                    location,
                    date,
                    status,
                    description
                FROM complaints
                ORDER BY id DESC
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            self.table.setRowCount(0)

            for row_number, row_data in enumerate(rows):

                self.table.insertRow(
                    row_number
                )

                for column_number, data in enumerate(
                    row_data
                ):

                    item = QTableWidgetItem(
                        str(data)
                    )

                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

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

    # ---------------- FIND MECHANIC ----------------
    def find_mechanic(self):

        selected = self.table.currentRow()

        # No complaint selected
        if selected == -1:

            QMessageBox.warning(
                self,
                "Error",
                "Please select a complaint row"
            )

            return

        # Column 3 = Category
        category = self.table.item(
            selected, 3
        ).text().lower()

        # Column 5 = Location
        location = self.table.item(
            selected, 5
        ).text().strip()

        # Decide which service to search
        if "fan" in category or "electric" in category:

            search = "electrician"

        elif "water" in category:

            search = "plumber"

        elif "chair" in category:

            search = "carpenter"

        elif "internet" in category:

            search = "wifi repair"

        else:

            search = "repair shop"

        # Add location
        if location:

            search = search + " near " + location

        else:

            search = search + " near me"

        # Create Google Maps URL
        url = (
            "https://www.google.com/maps/search/"
            + quote_plus(search)
        )

        # Open browser
        webbrowser.open(url)

    # ---------------- UPDATE STATUS ----------------
    def update_status(self):

        selected = self.table.currentRow()

        if selected == -1:

            QMessageBox.warning(
                self,
                "Error",
                "Please select complaint row"
            )

            return

        # ID is column 0
        complaint_id = self.table.item(
            selected, 0
        ).text()

        new_status = (
            self.status_box.currentText()
        )

        try:

            conn = self.connect_db()
            cursor = conn.cursor()

            query = """
                UPDATE complaints
                SET status=%s
                WHERE id=%s
            """

            cursor.execute(
                query,
                (
                    new_status,
                    complaint_id
                )
            )

            conn.commit()
            conn.close()

            QMessageBox.information(
                self,
                "Success",
                "Status Updated Successfully"
            )

            self.load_data()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    # ---------------- DELETE ----------------
    def delete_complaint(self):

        selected = self.table.currentRow()

        if selected == -1:

            QMessageBox.warning(
                self,
                "Error",
                "Select complaint first"
            )

            return

        complaint_id = self.table.item(
            selected, 0
        ).text()

        confirm = QMessageBox.question(
            self,
            "Confirm",
            "Delete selected complaint?"
        )

        if confirm == QMessageBox.Yes:

            try:

                conn = self.connect_db()
                cursor = conn.cursor()

                query = """
                    DELETE FROM complaints
                    WHERE id=%s
                """

                cursor.execute(
                    query,
                    (complaint_id,)
                )

                conn.commit()
                conn.close()

                QMessageBox.information(
                    self,
                    "Deleted",
                    "Complaint Deleted"
                )

                self.load_data()

            except Exception as e:

                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )


# ---------------- TEST ----------------
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = AdminWindow()
    window.show()

    sys.exit(app.exec_())