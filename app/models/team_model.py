from app.db import get_db

class TeamDAO:
    @staticmethod
    def create_team(team_name, leader_id):
        conn = get_db()
        cursor = conn.cursor()
        try:
            query_team = "INSERT INTO Teams (TeamName, LeaderID) VALUES (?, ?)"
            cursor.execute(query_team, (team_name, leader_id))
            
            cursor.execute("SELECT @@IDENTITY") 
            team_id = cursor.fetchone()[0]

            query_member = "INSERT INTO TeamMembers (TeamID, StudentID) VALUES (?, ?)"
            cursor.execute(query_member, (team_id, leader_id))

            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating team: {e}")
            conn.rollback()
            return False

    @staticmethod
    def get_team_by_leader(leader_id):
        """Checks if a student is already leading a team"""
        conn = get_db()
        cursor = conn.cursor()
        query = "SELECT * FROM Teams WHERE LeaderID = ?"
        cursor.execute(query, (leader_id,))
        return cursor.fetchone()

    @staticmethod
    def get_team_members(team_id):
        """Helper to show who is in the team"""
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT u.FullName, u.Email 
            FROM TeamMembers tm
            JOIN Users u ON tm.StudentID = u.UserID
            WHERE tm.TeamID = ?
        """
        cursor.execute(query, (team_id,))
        return cursor.fetchall()
    @staticmethod
    def add_member_by_email(team_id, student_email):
        """FR8: Invite student by email"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT UserID FROM Users WHERE Email = ? AND Role = 'Student'", (student_email,))
            student = cursor.fetchone()
            
            if not student:
                return "User not found or not a student"

            student_id = student[0]

            cursor.execute("SELECT * FROM TeamMembers WHERE StudentID = ?", (student_id,))
            if cursor.fetchone():
                return "Student is already in a team"

            cursor.execute("INSERT INTO TeamMembers (TeamID, StudentID) VALUES (?, ?)", (team_id, student_id))
            conn.commit()
            return "Success"
        except Exception as e:
            conn.rollback()
            return "Error adding member"