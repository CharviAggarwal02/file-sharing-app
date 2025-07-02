# Secure File Sharing App

A secure file sharing backend system built with **Flask** and **SQLite**, designed for two types of users:
- 👷 Ops Users: Upload `.pptx`, `.docx`, `.xlsx` files
- 👤 Client Users: Sign up, verify email, view files, and download them via secure encrypted links

# Features

- JWT-based Authentication
- Role-based Access Control (Ops vs Client)
- Secure file uploads and downloads
- Encrypted download links (valid per user)
- Email verification simulation
- SQLite database


# Tech Stack

- **Backend**: Flask
- **Database**: SQLite (via SQLAlchemy)
- **Auth**: Flask-JWT-Extended
- **Encryption**: itsdangerous
- **File Handling**: werkzeug


