from app.db import get_db
import hashlib

class UserDAO:

    @staticmethod
    def create_user(username, email, password, role):
        conn = get_db()
        cursor = conn.cursor()
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            query = """
                INSERT INTO Users (Username, Email, PasswordHash, Role)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (username, email, password_hash, role))

            return True
        except Exception as e:
            print(f"[DB Error] create_user(): {e}")
            return False

    @staticmethod
    def get_user_by_email(email):
        conn = get_db()
        cursor = conn.cursor()
        try:
            query = """
                SELECT UserID, Username, Email, PasswordHash, Role
                FROM Users
                WHERE Email = ?
            """
            cursor.execute(query, (email,))
            return cursor.fetchone()
        except Exception as e:
            print(f"[DB Error] get_user_by_email(): {e}")
            return None
    @staticmethod
    def get_all_users():
        """For Admin Dashboard: List everyone"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT UserID, FullName, Email, Role, CreatedAt FROM Users")
        return cursor.fetchall()

    @staticmethod
    def delete_user(user_id):
        """For Admin: Remove a user"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Delete failed: {e}")
            return False