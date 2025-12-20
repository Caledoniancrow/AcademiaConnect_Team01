from app.db import get_db

class MilestoneDAO:
    @staticmethod
    def create_milestone(project_id, title, description, deadline):
        conn = get_db()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Milestones (ProjectID, Title, Description, Deadline, Status)
                VALUES (?, ?, ?, ?, 'Pending')
            """
            cursor.execute(query, (project_id, title, description, deadline))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating milestone: {e}")
            return False

    @staticmethod
    def get_project_milestones(project_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Milestones WHERE ProjectID = ?", (project_id,))
        return cursor.fetchall()

    @staticmethod
    def submit_work(milestone_id, submission_link):
        """Student submits work"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            query = "UPDATE Milestones SET SubmissionLink = ?, Status = 'Submitted' WHERE MilestoneID = ?"
            cursor.execute(query, (submission_link, milestone_id))
            conn.commit()
            return True
        except:
            return False

    @staticmethod
    def grade_milestone(milestone_id, grade):
        """Supervisor/Industry grades the work"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            query = "UPDATE Milestones SET Grade = ?, Status = 'Graded' WHERE MilestoneID = ?"
            cursor.execute(query, (grade, milestone_id))
            conn.commit()
            return True
        except:
            return False