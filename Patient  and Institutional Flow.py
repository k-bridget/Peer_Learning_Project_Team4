import mysql.connector
import datetime
import schedule
import time
import uuid

# Establish a connection to MySQL database
def get_db_connection():
    """Establish and return a connection to the MySQL database."""
    return mysql.connector.connect(
        host="your_host",           # Replace with your MySQL host
        user="your_username",       # Replace with your MySQL username
        password="your_password",   # Replace with your MySQL password
        database="appointments_db"  # Replace with your database name
    )

def get_doctor_profiles():
    """Retrieve doctor profiles from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    
    if not doctors:
        print("No doctors available.")
    else:
        print("\nAvailable Doctors:")
        for doc in doctors:
            print(f"ID: {doc[0]} | Name: {doc[1]} | Specialty: {doc[2]}")

def check_availability(doctor_id):
    """Check availability of a specific doctor."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date, time FROM appointments WHERE doctor_id = %s", (doctor_id,))
    booked_slots = cursor.fetchall()
    conn.close()
    
    print("\nBooked Slots:")
    for slot in booked_slots:
        print(f"Date: {slot[0]} | Time: {slot[1]}")

def generate_meet_link():
    """Generate a mock Google Meet link."""
    return f"https://meet.google.com/{uuid.uuid4().hex[:10]}"

def book_appointment(patient_name, doctor_id, date, time):
    """Book an appointment while preventing double bookings."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the slot is already booked
    cursor.execute("SELECT * FROM appointments WHERE doctor_id = %s AND date = %s AND time = %s", (doctor_id, date, time))
    if cursor.fetchone():
        print("Sorry, this time slot is already booked. Please choose another.")
        conn.close()
        return
    
    meet_link = generate_meet_link()
    cursor.execute("INSERT INTO appointments (patient_name, doctor_id, date, time, meet_link) VALUES (%s, %s, %s, %s, %s)",
                   (patient_name, doctor_id, date, time, meet_link))
    conn.commit()
    conn.close()
    print(f"Appointment booked successfully! Your Google Meet link: {meet_link}")

def send_reminder():
    """Send appointment reminders."""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.date.today().strftime('%Y-%m-%d')
    cursor.execute("SELECT patient_name, date, time, meet_link FROM appointments WHERE date = %s", (today,))
    appointments = cursor.fetchall()
    conn.close()
    
    for appointment in appointments:
        print(f"Reminder: {appointment[0]}, you have an appointment today at {appointment[2]}. Join here: {appointment[3]}")

def schedule_reminders():
    """Schedule reminders to run every day at 8 AM."""
    schedule.every().day.at("08:00").do(send_reminder)
    while True:
        schedule.run_pending()
        time.sleep(60)

def patient_menu():
    """CLI Menu for patient interactions."""
    while True:
        print("\nPatient Menu:")
        print("1. View Doctor Profiles")
        print("2. Check Doctor Availability")
        print("3. Book an Appointment")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            get_doctor_profiles()
        elif choice == '2':
            doctor_id = input("Enter Doctor ID: ")
            check_availability(doctor_id)
        elif choice == '3':
            patient_name = input("Enter your name: ")
            doctor_id = input("Enter Doctor ID: ")
            date = input("Enter appointment date (YYYY-MM-DD): ")
            time = input("Enter appointment time (HH:MM): ")
            book_appointment(patient_name, doctor_id, date, time)
        elif choice == '4':
            print("Exiting patient menu.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    patient_menu()
