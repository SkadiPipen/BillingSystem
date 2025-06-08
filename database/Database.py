import sys
import os
import psycopg2
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

load_dotenv()

class DBConnector(QWidget): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Connector")
        self.setFixedSize(300, 100)
        self.connect_to_db()

    def get_connection(self):
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    def connect_to_db(self):
        try:
            conn = self.get_connection()
        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", f"Error:\n{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DBConnector()
    window.show()
    sys.exit(app.exec_())