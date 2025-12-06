from app.db import get_db

class ProjectDAO:

    @staticmethod
    def create_project(title, description, industry_id):
        conn = get_db()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Projects (Title, Description, Status, IndustryID)
                VALUES (?, ?, 'Open', ?)
            """
            cursor.execute(query, (title, description, industry_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"[DB Error] create_project(): {e}")
            return False

    @staticmethod
    def get_all_projects():
        conn = get_db()
        cursor = conn.cursor()
        try:
            query = """
                SELECT 
                    p.ProjectID,
                    p.Title,
                    p.Description,
                    p.Status,
                    u.Username AS CompanyName
                FROM Projects p
                JOIN Users u ON p.IndustryID = u.UserID
                ORDER BY p.ProjectID DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"[DB Error] get_all_projects(): {e}")
            return []
