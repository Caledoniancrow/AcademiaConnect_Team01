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
            return team_id
        except Exception as e:
            print(f"Error creating team: {e}")
            conn.rollback()
            return None

    @staticmethod
    def get_team_by_leader(leader_id):
        """Checks if a student is already leading a team"""
        conn = get_db()
        cursor = conn.cursor()
        query = "SELECT TeamID, TeamName FROM Teams WHERE LeaderID = ?"
        cursor.execute(query, (leader_id,))
        return cursor.fetchone()

    @staticmethod
    def get_teams_by_member(student_id):
        """Get all teams a student is part of"""
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT t.TeamID, t.TeamName, t.LeaderID, u.Username AS LeaderName
            FROM Teams t
            JOIN TeamMembers tm ON t.TeamID = tm.TeamID
            JOIN Users u ON t.LeaderID = u.UserID
            WHERE tm.StudentID = ?
        """
        cursor.execute(query, (student_id,))
        return cursor.fetchall()

    @staticmethod
    def get_team_members(team_id):
        """Get all members of a team"""
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT u.UserID, u.Username, u.Email, tm.StudentID
            FROM TeamMembers tm
            JOIN Users u ON tm.StudentID = u.UserID
            WHERE tm.TeamID = ?
        """
        cursor.execute(query, (team_id,))
        return cursor.fetchall()
    
    @staticmethod
    def get_team_details(team_id):
        """Get team info including leader"""
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT t.TeamID, t.TeamName, t.LeaderID, u.Username AS LeaderName
            FROM Teams t
            JOIN Users u ON t.LeaderID = u.UserID
            WHERE t.TeamID = ?
        """
        cursor.execute(query, (team_id,))
        return cursor.fetchone()
    
    @staticmethod
    def add_member_by_email(team_id, student_email, requester_id):
        """Add a member to team (only leader can do this)"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            # Check if requester is the leader
            cursor.execute("SELECT LeaderID FROM Teams WHERE TeamID = ?", (team_id,))
            team = cursor.fetchone()
            if not team or team[0] != requester_id:
                return "Only team leader can add members"

            # Find the student by email
            cursor.execute("SELECT UserID FROM Users WHERE Email = ? AND Role = 'Student'", (student_email,))
            student = cursor.fetchone()
            
            if not student:
                return "User not found or not a student"

            student_id = student[0]

            # Check if student is already in any team
            cursor.execute("SELECT * FROM TeamMembers WHERE StudentID = ?", (student_id,))
            if cursor.fetchone():
                return "Student is already in a team"

            # Add to team
            cursor.execute("INSERT INTO TeamMembers (TeamID, StudentID) VALUES (?, ?)", (team_id, student_id))
            conn.commit()
            return "Success"
        except Exception as e:
            conn.rollback()
            return f"Error adding member: {str(e)}"
    
    @staticmethod
    def remove_member(team_id, student_id, requester_id):
        """Remove a member from team (only leader can do this, cannot remove self)"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            # Check if requester is the leader
            cursor.execute("SELECT LeaderID FROM Teams WHERE TeamID = ?", (team_id,))
            team = cursor.fetchone()
            if not team or team[0] != requester_id:
                return "Only team leader can remove members"
            
            # Cannot remove leader
            if student_id == requester_id:
                return "Team leader cannot remove themselves"

            # Remove member
            cursor.execute("DELETE FROM TeamMembers WHERE TeamID = ? AND StudentID = ?", (team_id, student_id))
            conn.commit()
            return "Success"
        except Exception as e:
            conn.rollback()
            return f"Error removing member: {str(e)}"
    
    @staticmethod
    def delete_team(team_id, requester_id):
        """Delete a team (only leader can do this)"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            # Check if requester is the leader
            cursor.execute("SELECT LeaderID FROM Teams WHERE TeamID = ?", (team_id,))
            team = cursor.fetchone()
            if not team:
                return "Team not found"
            if team[0] != requester_id:
                return "Only team leader can delete the team"
            
            # Check if team has any applications
            cursor.execute("SELECT COUNT(*) FROM Applications WHERE TeamID = ?", (team_id,))
            app_count = cursor.fetchone()[0]
            
            if app_count > 0:
                return "Cannot delete team with existing applications"
            
            # Delete team members first (foreign key constraint)
            cursor.execute("DELETE FROM TeamMembers WHERE TeamID = ?", (team_id,))
            
            # Delete the team
            cursor.execute("DELETE FROM Teams WHERE TeamID = ?", (team_id,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(f"Error deleting team: {e}")
            conn.rollback()
            return "Error deleting team"