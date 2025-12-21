from app.db import get_db

class ApplicationDAO:
    @staticmethod
    def apply_to_project(team_id, project_id, faculty_id, proposal_text):
        """
        Student applies to a project AND selects a Faculty Supervisor.
        """
        conn = get_db()
        cursor = conn.cursor()
        try:
            # Check if team already applied to this project
            check_query = "SELECT * FROM Applications WHERE TeamID = ? AND ProjectID = ?"
            cursor.execute(check_query, (team_id, project_id))
            if cursor.fetchone():
                return False 

            query = """
                INSERT INTO Applications (TeamID, ProjectID, FacultyID, TeamStatement, Status) 
                VALUES (?, ?, ?, ?, 'Pending Review')
            """
            cursor.execute(query, (team_id, project_id, faculty_id, proposal_text))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error applying: {e}")
            conn.rollback()
            return False

    @staticmethod
    def get_applications_for_faculty(faculty_id):
        """
        Faculty sees applications specifically sent to THEM.
        """
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT 
                a.ApplicationID, 
                t.TeamName, 
                p.Title AS ProjectTitle, 
                a.TeamStatement, 
                a.Status,
                a.ApplicationDate,
                p.ProjectID,
                a.TeamID
            FROM Applications a
            JOIN Teams t ON a.TeamID = t.TeamID
            JOIN Projects p ON a.ProjectID = p.ProjectID
            WHERE a.FacultyID = ? AND a.Status = 'Pending Review'
        """
        cursor.execute(query, (faculty_id,))
        return cursor.fetchall()
    
    @staticmethod
    def get_applications_for_industry(industry_id):
        """
        Industry sees applications for their projects that faculty approved.
        """
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT 
                a.ApplicationID, 
                t.TeamName, 
                p.Title AS ProjectTitle, 
                a.TeamStatement, 
                a.Status,
                a.ApplicationDate,
                p.ProjectID,
                a.TeamID
            FROM Applications a
            JOIN Teams t ON a.TeamID = t.TeamID
            JOIN Projects p ON a.ProjectID = p.ProjectID
            WHERE p.IndustryID = ? AND a.Status = 'Faculty Approved'
        """
        cursor.execute(query, (industry_id,))
        return cursor.fetchall()
    
    @staticmethod
    def get_applications_by_user(user_id):
        """
        Get applications for the logged-in student (via their team).
        """
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT 
                a.ApplicationID, 
                p.Title, 
                a.Status, 
                t.TeamName,
                p.ProjectID
            FROM Applications a
            JOIN Projects p ON a.ProjectID = p.ProjectID
            JOIN Teams t ON a.TeamID = t.TeamID
            JOIN TeamMembers tm ON t.TeamID = tm.TeamID
            WHERE tm.StudentID = ?
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    @staticmethod
    def update_status(app_id, new_status):
        conn = get_db()
        cursor = conn.cursor()
        try:
            query = "UPDATE Applications SET Status = ? WHERE ApplicationID = ?"
            cursor.execute(query, (new_status, app_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating status: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def get_application_details(app_id):
        """Get detailed info about an application"""
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT 
                a.ApplicationID,
                a.TeamStatement,
                a.Status,
                t.TeamName,
                t.TeamID,
                p.Title AS ProjectTitle,
                p.Description AS ProjectDescription,
                u.Username AS IndustryName
            FROM Applications a
            JOIN Teams t ON a.TeamID = t.TeamID
            JOIN Projects p ON a.ProjectID = p.ProjectID
            JOIN Users u ON p.IndustryID = u.UserID
            WHERE a.ApplicationID = ?
        """
        cursor.execute(query, (app_id,))
        return cursor.fetchone()