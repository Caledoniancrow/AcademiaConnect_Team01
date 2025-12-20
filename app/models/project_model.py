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

    @staticmethod
    def get_pending_projects():
        """FR6: For Admin to vet projects"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Projects WHERE Status = 'Pending'")
        return cursor.fetchall()

    @staticmethod
    def approve_project(project_id):
        """FR6: Admin approves a proposal"""
        conn = get_db()
        cursor = conn.cursor()
        query = "UPDATE Projects SET Status = 'Approved' WHERE ProjectID = ?"
        cursor.execute(query, (project_id,))
        conn.commit()
        return True

    @staticmethod
    def filter_projects(skill=None, funding_min=None):
        """FR7: Filter by Skill and Funding"""
        conn = get_db()
        cursor = conn.cursor()
        
        query = "SELECT * FROM Projects WHERE Status = 'Approved'"
        params = []

        if skill:
            query += " AND RequiredSkills LIKE ?"
            params.append(f"%{skill}%")
        
        if funding_min:
            query += " AND FundingAmount >= ?"
            params.append(funding_min)

        cursor.execute(query, tuple(params))
        return cursor.fetchall()