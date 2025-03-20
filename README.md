# Habit Tracker

#### Video Demo: https://youtu.be/HcHheAYiY9w

#### Description:

# Secure Habit Tracker

This project is a Flask-based habit tracker web application that enables users to register, log in, and add personal habits securely. The application has been built with a focus on modern security practices and includes the following key features:

- **Secure User Authentication:**  
  Users register and log in using a system that securely hashes passwords with Werkzeug's `generate_password_hash` and verifies them with `check_password_hash`. This ensures that plain-text passwords are never stored.

- **Data Encryption:**  
  All habit data entered by the user is encrypted using the Cryptography library's Fernet module before being stored in the SQLite database. This ensures that sensitive user information remains confidential, even if the database is compromised.

- **SQL Injection Prevention:**  
  The application uses parameterized SQL queries for all database interactions, effectively mitigating the risk of SQL injection attacks.

- **User-Friendly Interface:**  
  The web interface is built using Flask templates and includes clear navigation for registration, login, adding habits, and viewing your dashboard.

This secure habit tracker demonstrates practical experience in secure web development and is an excellent example of applying security best practices in a real-world application.
