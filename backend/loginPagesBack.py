from repositories.user_repository import UserRepository
import psycopg2

class LoginPagesBack:
    def __init__(self):
        # Initialize DB connection
        self.conn = psycopg2.connect(
            dbname="billingSystem",
            user="postgres",
            password="egoist123",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def checkUserType(self, username, password):
        user_repository = UserRepository()
        result = user_repository.check_user(username, password)

        # ✅ Insert log only if login is successful
        if result:
            try:
                self.cur.execute("""
                    INSERT INTO system_logs (message, user_name)
                    VALUES (%s, %s)
                """, ("User logged in", username))
                self.conn.commit()
            except Exception as e:
                print(f"Error logging login event: {e}")

        return result

    def gmail_exists(self, gmail):
        self.cur.execute("SELECT 1 FROM users WHERE gmail = %s", (gmail,))
        return self.cur.fetchone() is not None

    def update_password_by_gmail(self, gmail, new_password):
        try:
            self.cur.execute("UPDATE users SET password = %s WHERE gmail = %s", (new_password, gmail))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
