import mysql.connector
from mysql.connector import Error
import uuid
from datetime import datetime, timedelta

class AppointmentSystem:
    def __init__(self):
        """Initialize the appointment system and set up the database connection."""
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'school',
            'database': 'mindsafe'
        }
        self._initialize_database()
        
    def _create_connection(self):
        """Create and return a MySQL database connection."""
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def _initialize_database(self):
        """Initialize database tables if they don't exist."""
        conn = self._create_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id VARCHAR(36) PRIMARY KEY,
                    patient VARCHAR(255) NOT NULL,
                    doctor VARCHAR(255) NOT NULL,
                    appointment_time DATETIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        except Error as e:
            print(f"Database initialization error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def book_appointment(self):
        """Handle appointment booking user flow."""
        print("\n--- Book New Appointment ---")
        patient = input("Enter patient name: ")
        doctor = input("Enter doctor name: ")
        
        while True:
            try:
                days = int(input("How many days from now? (1-30): "))
                if 1 <= days <= 30:
                    break
                print("Please enter a number between 1 and 30.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        appointment_time = datetime.now() + timedelta(days=days)
        appointment_id = str(uuid.uuid4())

        conn = self._create_connection()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointments (id, patient, doctor, appointment_time)
                VALUES (%s, %s, %s, %s)
            """, (appointment_id, patient, doctor, appointment_time.strftime("%Y-%m-%d %H:%M:%S")))
            
            conn.commit()
            print(f"\nAppointment booked for {patient} with {doctor} on {appointment_time.strftime('%Y-%m-%d %H:%M')}.")
            
        except Error as e:
            print(f"Booking failed: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def view_appointments(self):
        """Show upcoming appointments."""
        conn = self._create_connection()
        if conn is None:
            return

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM appointments 
                WHERE appointment_time > NOW()
                ORDER BY appointment_time ASC
            """)
            
            appointments = cursor.fetchall()
            
            if not appointments:
                print("\nNo upcoming appointments found.")
                return
                
            print("\n--- Upcoming Appointments ---")
            for appt in appointments:
                print(f"\nID: {appt['id']}")
                print(f"Patient: {appt['patient']}")
                print(f"Doctor: {appt['doctor']}")
                print(f"Time: {appt['appointment_time'].strftime('%Y-%m-%d %H:%M')}")
                print("─" * 30)
                
        except Error as e:
            print(f"Error retrieving appointments: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def check_reminders(self):
        """Check for appointments within the next 24 hours."""
        conn = self._create_connection()
        if conn is None:
            return

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM appointments 
                WHERE appointment_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 1 DAY)
                ORDER BY appointment_time ASC
            """)
            
            upcoming = cursor.fetchall()
            
            if not upcoming:
                print("\nNo appointments in the next 24 hours.")
                return
                
            print("\nUpcoming Appointments (Next 24 Hours):")
            for appt in upcoming:
                print(f"\n{appt['patient']} with {appt['doctor']} at {appt['appointment_time'].strftime('%H:%M')}")
                
        except Error as e:
            print(f"Error checking reminders: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

def main_menu():
    """Main menu for the appointment system."""
    system = AppointmentSystem()
    
    while True:
        print("\nAppointment Management System")
        print("1. Book New Appointment")
        print("2. View Upcoming Appointments")
        print("3. Check Reminders")
        print("4. Exit")
        
        choice = input("\nYour choice: ")
        
        if choice == '1':
            system.book_appointment()
        elif choice == '2':
            system.view_appointments()
        elif choice == '3':
            system.check_reminders()
        elif choice == '4':
            print("\nThank you for using the system!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
    