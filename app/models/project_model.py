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
            conn.rollback()
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
    def get_project_by_id(project_id):
        """Get a single project by ID"""
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
                WHERE p.ProjectID = ?
            """
            cursor.execute(query, (project_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"[DB Error] get_project_by_id(): {e}")
            return None
    
    @staticmethod
    def get_projects_by_industry(industry_id):
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
                WHERE p.IndustryID = ?
                ORDER BY p.ProjectID DESC
            """
            cursor.execute(query, (industry_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"[DB Error] get_projects_by_industry(): {e}")
            return []
    
    @staticmethod
    def delete_project(project_id, industry_id):
        """Delete a project (only the owner can delete)"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            # First check if this industry owns the project
            cursor.execute("SELECT IndustryID FROM Projects WHERE ProjectID = ?", (project_id,))
            project = cursor.fetchone()
            
            if not project:
                return "Project not found"
            
            if project[0] != industry_id:
                return "You can only delete your own projects"
            
            # Check if there are any applications
            cursor.execute("SELECT COUNT(*) FROM Applications WHERE ProjectID = ?", (project_id,))
            app_count = cursor.fetchone()[0]
            
            if app_count > 0:
                return "Cannot delete project with existing applications"
            
            # Delete the project
            cursor.execute("DELETE FROM Projects WHERE ProjectID = ?", (project_id,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(f"[DB Error] delete_project(): {e}")
            conn.rollback()
            return "Error deleting project"
    
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