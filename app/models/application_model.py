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
            check_query = "SELECT * FROM Applications WHERE TeamID = ? AND ProjectID = ?"
            cursor.execute(check_query, (team_id, project_id))
            if cursor.fetchone():
                return False 

            query = """
                INSERT INTO Applications (TeamID, ProjectID, FacultyID, TeamStatement, Status) 
                VALUES (?, ?, ?, ?, 'Pending Faculty')
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
        FR10: Faculty sees applications specifically sent to THEM.
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
                a.ApplicationDate
            FROM Applications a
            JOIN Teams t ON a.TeamID = t.TeamID
            JOIN Projects p ON a.ProjectID = p.ProjectID
            WHERE a.FacultyID = ? AND a.Status = 'Pending Faculty'
        """
        cursor.execute(query, (faculty_id,))
        return cursor.fetchall()

    @staticmethod
    def update_status(app_id, new_status):
        conn = get_db()
        cursor = conn.cursor()
        query = "UPDATE Applications SET Status = ? WHERE ApplicationID = ?"
        cursor.execute(query, (new_status, app_id))
        conn.commit()
        return True