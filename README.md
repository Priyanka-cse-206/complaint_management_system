# 📋 Complaint Management System

A desktop-based **Complaint Management System** built with **Python** and **PyQt5**, designed to streamline the process of registering, tracking, and resolving complaints through dedicated **User** and **Admin** interfaces.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PyQt5-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status" />
</p>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 📌 About the Project

The **Complaint Management System** is a Python desktop application built using the **PyQt5** framework. It provides a clean, GUI-driven workflow that allows users to submit and track complaints, while giving administrators the tools to review, manage, and resolve them efficiently — eliminating the need for manual, paper-based complaint tracking.

The system supports two distinct roles:

- 👤 **User** — Register/login, submit new complaints, and track the status of previously submitted complaints.
- 🛠️ **Admin** — Login to a dedicated dashboard to view all submitted complaints, update their status, and manage resolutions.

---

## ✨ Features

- 🔐 **Dual Authentication** — Separate secure login flows for Users and Admins
- 📝 **Complaint Submission** — Simple form-based complaint registration
- 📊 **Status Tracking** — Users can check whether a complaint is Pending, In Progress, or Resolved
- 🗂️ **Admin Dashboard** — Centralized view to manage and update all complaints
- 💾 **Persistent Storage** — Complaint and user data stored in a local database
- 🖥️ **Native Desktop GUI** — Responsive and intuitive interface built with PyQt5 widgets
- ⚡ **Lightweight** — No web server or browser required; runs as a standalone desktop app

---

## 🛠️ Tech Stack

| Layer            | Technology       |
|-------------------|-----------------|
| Language           | Python 3.x       |
| GUI Framework      | PyQt5            |
| Database           |  MySQL  |
| IDE                | VS Code |

---

## 📁 Project Structure

```
complaint_management_system/
│
├── login.py               
├── complaint.py                     
├── home.py              
├── admin.py              
├── my_complaints.py             
└── README.md                 # Project documentation
```

> ℹ️ Update this structure to match your actual folder layout if it differs.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed on your system:

- [Python 3.8+](https://www.python.org/downloads/)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Priyanka-cse-206/complaint_management_system.git
   cd complaint_management_system
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # On Windows
   source venv/bin/activate   # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` yet, at minimum install:
   ```bash
   pip install PyQt5
   ```

### Running the Application

```bash
python main.py
```

---

## 💻 Usage

1. Launch the application using `python main.py`.
2. **New users** can register an account; **existing users** can log in directly.
3. Submit a complaint through the complaint form, providing the relevant details.
4. Track the real-time status of your submitted complaints from the dashboard.
5. **Admins** log in through the Admin panel to view all complaints, update statuses, and mark issues as resolved.



## 🤝 Contributing

Contributions make the open-source community a great place to learn and build. Any contributions are **greatly appreciated**.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 📬 Contact

**Priyanka** — [GitHub Profile](https://github.com/Priyanka-cse-206)

Project Link: [https://github.com/Priyanka-cse-206/complaint_management_system](https://github.com/Priyanka-cse-206/complaint_management_system)

---

<p align="center">⭐ If you found this project useful, consider giving it a star!</p>
