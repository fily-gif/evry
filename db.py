import sqlite3

class UserDatabase:
    def __init__(self, database_filename: str):
        # Connect to the database
        self.conn = sqlite3.connect(database_filename)

        # Create a cursor to execute SQL commands
        self.cursor = self.conn.cursor()

        # Create the table if it does not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY,
                name TEXT NOT NULL,
                reputation INT NOT NULL DEFAULT 0
            );
        ''')

        self.conn.commit()

    def add_user(self, user_id: str, name: str):
        sql = "INSERT INTO users (user_id, name) VALUES (?, ?)"
        values = (user_id, name)

        # Insert the user data into the table
        self.cursor.execute(sql, values)

        # Commit the changes to the database
        self.conn.commit()

    def search_user(self, user_id: str):
        sql = "SELECT * FROM users WHERE user_id=?"
        values = (user_id,)

        # Execute the SELECT statement to search for the user
        self.cursor.execute(sql, values)

        # Fetch the result of the SELECT statement
        user = self.cursor.fetchone()

        if user:
            return True
        else:
            return False

    def add_reputation(self, user_id: str, rep_amount: int):
        sql = "UPDATE users SET reputation = reputation + ? WHERE user_id=?"
        values = (rep_amount, user_id)

        # Update user's reputation
        self.cursor.execute(sql, values)

        # Commit the changes to the database
        self.conn.commit()

    def get_reputation(self, user_id: str):
        sql = "SELECT reputation FROM users WHERE user_id=?"
        values = (user_id,)

        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()

        self.conn.commit()

        if result:
            return result[0]
        else:
            return None

'''
# Example usage
database = UserDatabase(database_filename)
database.add_user(1, 'John Doe')
database.search_user(2)
database.add_reputation(3, 1)
database.get_reputation(4)'''
