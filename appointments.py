import sqlite3
import uuid
from datetime import datetime, timezone, timedelta
import subprocess

# Initialize database
conn = sqlite3.connect("appointments.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id TEXT PRIMARY KEY,
    patient TEXT,
    doctor TEXT,
    time TEXT
)
""")
conn.commit()

# Function to book an appointment
def book_appointment(patient, doctor, days_from_now):
    appointment_time = datetime.now(timezone.utc) + timedelta(days=days_from_now)
    appointment_id = str(uuid.uuid4())

    cursor.execute("INSERT INTO appointments VALUES (?, ?, ?, ?)", 
                   (appointment_id, patient, doctor, appointment_time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    print(f"Appointment booked for {patient} with {doctor} on {appointment_time}.")

# Function to send reminders using a subprocess
def send_reminders():
    subprocess.run(["echo", "Reminder: You have an appointment soon!"])  # Simulating a cron job

# Booking an appointment
book_appointment("Alice", "Dr. Smith", 2)

# Run reminder system
send_reminders()

# Close the database connection
conn.close()