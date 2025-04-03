from colorama import Fore, Style, init
import mysql.connector
from mysql.connector import connect, Error

from sysAdmin.main import sys_menu
from instAdmin.main import init_menu
from doctor.main import handle_doctor_login
from user.main import handle_patient_login

init(autoreset= True) #initialzing Colorama

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
    
    def _simple_hash(self, data):
        """Basic reversible transformation (not secure - for demonstration only)"""
        shifted = ''.join(chr(ord(c) + 3) for c in data)
        return shifted[::-1]
    
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
        # Admin tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Admins (
                organisational_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Admin_Security_Questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                question VARCHAR(255) NOT NULL,
                answer VARCHAR(255) NOT NULL,
                FOREIGN KEY (email) REFERENCES Admins(email)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Admin_Recovery_Log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (email) REFERENCES Admins(email)
            )
        ''')
        
        # Doctor tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Appointment tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Rating tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                rating_id INT AUTO_INCREMENT PRIMARY KEY,
                doctor_name VARCHAR(255) NOT NULL,
                rating INT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
    # Doctor management methods
    def add_doctor(self, email, name, password):
        """Add new doctor to system"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            hashed_pw = self._simple_hash(password)
            cursor.execute('''
                INSERT INTO doctors (email, name, password)
                VALUES (%s, %s, %s)
            ''', (email, name, hashed_pw))
            conn.commit()
            return "Doctor added successfully!"
        except mysql.connector.Error as err:
            return f"Error adding doctor: {err}"
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def delete_doctor(self, email):
        """Remove doctor from system"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctors WHERE email = %s", (email,))
            conn.commit()
            return "Doctor deleted!" if cursor.rowcount else "Doctor not found!"
        except mysql.connector.Error as err:
            return f"Deletion failed: {err}"
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Appointment methods
    def get_all_appointments(self):
        """Retrieve all appointment records"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, appointment_id, 
                DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:%%i:%%s') AS formatted_ts
                FROM appointments
                ORDER BY timestamp DESC
            ''')
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching appointments: {err}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Rating methods
    def get_performance_ratings(self):
        """Retrieve all performance ratings"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT rating_id, doctor_name, rating,
                DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:%%i:%%s') AS formatted_ts
                FROM ratings
                ORDER BY rating_id DESC
            ''')
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching ratings: {err}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Admin methods
    def register_admin(self, org_name, email, password, questions, answers):
        """Admin registration with security questions"""
        hashed_pw = self._simple_hash(password)
        hashed_answers = [self._simple_hash(ans.lower()) for ans in answers]

        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT email FROM Admins WHERE email = %s", (email,))
            if cursor.fetchone():
                return "Email already registered"
            
            cursor.execute('''
                INSERT INTO Admins (organisational_name, email, password)
                VALUES (%s, %s, %s)
            ''', (org_name, email, hashed_pw))
            
            for q, a in zip(questions, hashed_answers):
                cursor.execute('''
                    INSERT INTO Admin_Security_Questions (email, question, answer)
                    VALUES (%s, %s, %s)
                ''', (email, q, a))
            
            conn.commit()
            return "Admin registration successful"
        except mysql.connector.Error as err:
            return f"Registration failed: {err}"
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def recover_admin_password(self, email):
        """Admin password recovery flow"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT email FROM Admins WHERE email = %s", (email,))
            if not cursor.fetchone():
                return "Admin not found"
            
            cursor.execute('''
                SELECT question FROM Admin_Security_Questions
                WHERE email = %s
            ''', (email,))
            questions = [row[0] for row in cursor.fetchall()]
            
            user_answers = [self._simple_hash(input(f"{q}: ").lower()) 
                        for q in questions]
            
            cursor.execute('''
                SELECT answer FROM Admin_Security_Questions
                WHERE email = %s
            ''', (email,))
            stored_answers = [row[0] for row in cursor.fetchall()]
            
            if user_answers != stored_answers:
                return "Security verification failed"
            
            new_password = input("Enter new password: ")
            hashed_new = self._simple_hash(new_password)
            
            cursor.execute('''
                UPDATE Admins
                SET password = %s
                WHERE email = %s
            ''', (hashed_new, email))
            
            cursor.execute('''
                INSERT INTO Admin_Recovery_Log (email)
                VALUES (%s)
            ''', (email,))
            
            conn.commit()
            return "Password reset successful"
        except mysql.connector.Error as err:
            return f"Recovery failed: {err}"
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    def list_doctors(self):
        """List all doctors in the system"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email, name FROM doctors")
            doctors = cursor.fetchall()
            
            if not doctors:
                print("No doctors found.")
                return
            
            print("\n--- All Doctors ---")
            for idx, doctor in enumerate(doctors, 1):
                print(f"{idx}. Email: {doctor[0]}, Name: {doctor[1]}")
                
        except mysql.connector.Error as err:
            print(f"Error listing doctors: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    def update_doctor_password(self, email, new_password):
        """Update doctor credentials"""
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            hashed_pw = self._simple_hash(new_password)
            cursor.execute('''
                UPDATE doctors
                SET password = %s
                WHERE email = %s
            ''', (hashed_pw, email))
            conn.commit()
            return "Credentials updated!" if cursor.rowcount else "Doctor not found!"
        except mysql.connector.Error as err:
            return f"Update failed: {err}"
        finally:
            if conn.is_connected():
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


def menu():    
    while True:
        print(Fore.YELLOW + r"""
         ___ ___  ____  ____   ___   _____  ____  _____  ___ 
        |   |   ||    ||    \ |   \ / ___/ /    ||     |/  _]
        | _   _ | |  | |  _  ||    (   \_ |  o  ||   __/  [_ 
        |  \_/  | |  | |  |  ||  D  \__  ||     ||  |_|    _]
        |   |   | |  | |  |  ||     /  \ ||  _  ||   _]   [_ 
        |   |   | |  | |  |  ||     \    ||  |  ||  | |     |
        |___|___||____||__|__||_____|\___||__|__||__| |_____|
        """)
        print(f"\n{Fore.MAGENTA}Mental Health Anonymous Booking System")
        print(f"\n{Fore.CYAN}1.Patient Portal")
        print(f"{Fore.GREEN}2.Doctor Portal")
        print(f"{Fore.RED}3.Institutional Admin Portal")
        print(f"{Fore.BLUE}4.System Admin Portal")
        print(f"{Fore.WHITE}5.Exit")
        
        choice = input(f"\nSelect your Portal: ")
        
        if choice == '1':
            handle_patient_login()
        elif choice == '2':
            handle_doctor_login()
        elif choice == '3':
            init_menu(auth)
        elif choice == '4':
            sys_menu(auth)
        elif choice == '5':
            print(f"{Fore.YELLOW}Exiting system...")
            break
        else:
            print(f"{Fore.RED}Invalid choice!")


if __name__ == "__main__":
    auth = AuthSystem(
        host="localhost",
        user="root",
        password="school",
        database="mindsafe"
    )
    menu()