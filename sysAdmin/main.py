import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent))

from monitor.sysmonitor import monitoring
from helpreq.request import get_request
from recovered.recovered import recovered_menu

import mysql.connector
from mysql.connector import connect, Error

class AuthSystem:
    def __init__(self, host, user, password, database):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self._initialize_database()
        
    def _create_connection(self):
        return mysql.connector.connect(**self.db_config)
    
    def _initialize_database(self):
        """Initialize database tables"""
        conn = self._create_connection()
        cursor = conn.cursor()
        
        # Create help_requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS help_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL
            )
        ''')
        
        # Security Questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Security_Questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                question VARCHAR(255) NOT NULL,
                answer VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        
        # Recovered Password log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recovered_password (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()

    def get_recovery_records(self):
        """Retrieve all password recovery records"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
        
            cursor.execute('''
                SELECT id, user_id, 
                DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:%%i:%%s') AS timestamp
                FROM recovered_password
                ORDER BY timestamp DESC
            ''')
            return cursor.fetchall()
        
        except mysql.connector.Error as err:
            print(f"Error fetching records: {err}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def get_all_help_requests(self):
        """Retrieve all help requests"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, user_id, message, 
                DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:%%i:%%s') AS timestamp
                FROM help_requests
                ORDER BY timestamp DESC
            ''')
            return cursor.fetchall()
            
        except mysql.connector.Error as err:
            print(f"Error fetching requests: {err}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

def sys_menu(auth_system):
 
    while True:
        print()
        print()
        print()
        print("1. System Monitoring")
        print("2. Help Request")
        print("3. Users")
        print("4. Password Recovered")
        print("5. Logout")
        choice = input("Your choice >>> ")

        if choice == '1':
            monitoring()
        elif choice == '2':
            get_request(auth_system)
        elif choice == '3':
            user()
        elif choice == '4':
            recovered_menu(auth_system)
        elif choice == '5':
            print("Logging out....")
            break
        else:
            print("Invalid input.")


if __name__ == "__main__":
    auth = AuthSystem(
        host="localhost",
        user="root",
        password="school",
        database="mindsafe"
    )
    sys_menu(auth)

