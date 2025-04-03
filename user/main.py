from colorama import Fore, init 
import threading
from .authsys import auth_menu
import time, sys
import mysql.connector
from mysql.connector import connect, Error



init(autoreset=True)

def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="school",
        database="mindsafe"
    )

class BlogManager:
    def __init__(self, conn):
        self.conn = conn
        self.current_blog = ""
        self.lock = threading.Lock()
        self.running = True
        self.update_event = threading.Event()
        
        # Start blog update thread
        self.thread = threading.Thread(target=self.update_blog, daemon=True)
        self.thread.start()

    def update_blog(self):
        while self.running:
            try:
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT b.content, d.name 
                    FROM blogs b
                    JOIN doctors d ON b.doctor_id = d.doctor_id
                    ORDER BY RAND() LIMIT 1
                """)
                blog = cursor.fetchone()
                
                with self.lock:
                    if blog:
                        self.current_blog = (
                            f"{Fore.MAGENTA}Latest Health Tip from Dr. {blog['name']}:\n"
                            f"{Style.RESET_ALL}{blog['content']}\n"
                            f"{Fore.CYAN}―" * 50
                        )
                    else:
                        self.current_blog = f"{Fore.YELLOW}No health tips available at the moment"
                    
                    # Trigger screen update
                    self.update_event.set()

                time.sleep(50)
                
            except Exception as e:
                with self.lock:
                    self.current_blog = f"{Fore.RED}Error loading health tips"
                self.update_event.set()
            finally:
                cursor.close()

    def stop(self):
        self.running = False
        self.thread.join()

class PatientPortal:
    def __init__(self, patient_data):
        self.patient = patient_data
        self.conn = create_db_connection()
        self.active = True
        self.blog_manager = BlogManager(self.conn)
        
    def display_menu(self):
        while self.active:
            # Clear previous blog content using ANSI escape codes
            sys.stdout.write("\033[8;0H\033[J")  # Move cursor to line 8 and clear below
            self.display_header()
            
            # Check if blog needs update
            if self.blog_manager.update_event.is_set():
                with self.blog_manager.lock:
                    print(self.blog_manager.current_blog)
                    self.blog_manager.update_event.clear()
            
            # Display menu options
            print(f"\n{Fore.CYAN}1. Appointments")
            print(f"{Fore.CYAN}2. My Profile")
            print(f"{Fore.CYAN}3. Help Requests")
            print(f"{Fore.CYAN}4. Rate Sessions")
            print(f"{Fore.RED}5. Logout")
            
            # Get user input without blocking
            choice = input(f"\n{Fore.WHITE}Enter your choice >>> ")
            self.handle_choice(choice)

    def display_header(self):
        # Static ASCII art and header
        print(Fore.MAGENTA + r'''
         _ _ ___ ___ ___    ___ ___ ___| |_ ___| |
        | | |_ -| -_|  _|  | . | . |  _|  _| .'| |
        |___|___|___|_|    |  _|___|_| |_| |__,|_|
                           |_|                    
        ''')
        print(f"\n{Fore.BLUE}Welcome, {self.patient['user_id']}!")

    def handle_choice(self, choice):        
            choice = input(Fore.WHITE + "\nYour choice >>> ")

            if choice == '1':
                self.manage_appointments()
            elif choice == '2':
                self.view_profile()
            elif choice == '3':
                self.manage_help_requests()
            elif choice == '4':
                self.rate_session()
            elif choice == '5':
                self.logout()
            else:
                print(Fore.RED + "Invalid input. Please try again.")

    def manage_appointments(self):
        while True:
            print(Fore.CYAN + "\nAppointment Management")
            print(Fore.YELLOW + "1. Book New Appointment")
            print(Fore.YELLOW + "2. View Upcoming Appointments")
            print(Fore.YELLOW + "3. View Reminders")
            print(Fore.YELLOW + "4. Back to Main Menu")
            
            choice = input(Fore.WHITE + "Your choice >>> ")
            
            if choice == '1':
                self.book_appointment()
            elif choice == '2':
                self.view_upcoming_appointments()
            elif choice == '3':
                self.view_reminders()
            elif choice == '4':
                break
            else:
                print(Fore.RED + "Invalid choice!")

    def book_appointment(self):
        try:
            # Show available sessions
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.*, d.name 
                FROM doctor_sessions s
                JOIN doctors d ON s.doctor_id = d.doctor_id
                WHERE s.booked = 0 AND s.start_time > NOW()
            """)
            sessions = cursor.fetchall()
            
            if not sessions:
                print(Fore.YELLOW + "No available sessions")
                return
                
            print(Fore.CYAN + "\nAvailable Sessions:")
            for idx, session in enumerate(sessions, 1):
                print(f"\n{idx}. Doctor: {session['name']}")
                print(f"  Time: {session['start_time']} to {session['end_time']}")
                print(f"  Gender Preference: {session['gender']}")

            selection = int(input("\nSelect session number: ")) - 1
            selected = sessions[selection]

            # Book appointment
            cursor.execute("""
                INSERT INTO appointments 
                (user_id, session_id, booked_at)
                VALUES (%s, %s, NOW())
            """, (self.patient['user_id'], selected['session_id']))
            
            # Mark session as booked
            cursor.execute("""
                UPDATE doctor_sessions 
                SET booked = 1 
                WHERE session_id = %s
            """, (selected['session_id'],))
            
            self.conn.commit()
            print(Fore.GREEN + "Appointment booked successfully!")
            
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def view_upcoming_appointments(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.*, d.name, s.meet_link 
                FROM appointments a
                JOIN doctor_sessions s ON a.session_id = s.session_id
                JOIN doctors d ON s.doctor_id = d.doctor_id
                WHERE a.user_id = %s AND s.start_time > NOW()
            """, (self.patient['user_id'],))
            
            appointments = cursor.fetchall()
            
            if not appointments:
                print(Fore.YELLOW + "No upcoming appointments")
                return
                
            print(Fore.CYAN + "\nUpcoming Appointments:")
            for appt in appointments:
                print(f"\nDoctor: {appt['name']}")
                print(f"Time: {appt['start_time']}")
                print(f"Meet Link: {appt['meet_link']}")
                
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def view_reminders(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.*, d.name, s.meet_link 
                FROM appointments a
                JOIN doctor_sessions s ON a.session_id = s.session_id
                JOIN doctors d ON s.doctor_id = d.doctor_id
                WHERE a.user_id = %s 
                AND s.start_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 1 DAY)
            """, (self.patient['user_id'],))
            
            reminders = cursor.fetchall()
            
            if not reminders:
                print(Fore.YELLOW + "No upcoming reminders")
                return
                
            print(Fore.CYAN + "\nAppointment Reminders:")
            for rem in reminders:
                print(f"\nDoctor: {rem['name']}")
                print(f"Time: {rem['start_time']}")
                print(f"Meet Link: {rem['meet_link']}")
                
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def view_profile(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Users WHERE user_id = %s", 
                          (self.patient['user_id'],))
            profile = cursor.fetchone()
            
            print(Fore.CYAN + "\nYour Profile:")
            print(f"User ID: {profile['user_id']}")
            print(f"Registered Email: {profile['email']}")
            
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def manage_help_requests(self):
        try:
            message = input("Enter your help request: ")
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO help_requests 
                (user_id, message, timestamp)
                VALUES (%s, %s, NOW())
            """, (self.patient['user_id'], message))
            self.conn.commit()
            print(Fore.GREEN + "Help request submitted successfully!")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def rate_session(self):
        try:
            # Show rateable sessions
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.*, d.name 
                FROM appointments a
                JOIN doctor_sessions s ON a.session_id = s.session_id
                JOIN doctors d ON s.doctor_id = d.doctor_id
                WHERE a.user_id = %s AND s.end_time < NOW()
            """, (self.patient['user_id'],))
            
            sessions = cursor.fetchall()
            
            if not sessions:
                print(Fore.YELLOW + "No sessions available for rating")
                return
                
            print(Fore.CYAN + "\nCompleted Sessions:")
            for idx, session in enumerate(sessions, 1):
                print(f"{idx}. Doctor: {session['name']} - {session['start_time']}")

            selection = int(input("\nSelect session to rate: ")) - 1
            selected = sessions[selection]
            
            rating = int(input("Rate this session (1-10): "))
            while rating < 1 or rating > 10:
                rating = int(input("Invalid rating! Please enter between 1-10: "))
            
            cursor.execute("""
                INSERT INTO ratings 
                (doctor_id, patient_id, rating, timestamp)
                VALUES (%s, %s, %s, NOW())
            """, (selected['doctor_id'], self.patient['user_id'], rating))
            
            self.conn.commit()
            print(Fore.GREEN + "Rating submitted successfully!")
            
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def logout(self):
        self.conn.close()
        self.active = False
        print(Fore.GREEN + "Logging out...")

# Add to handle_patient_login function:

def handle_patient_login():
    conn = create_db_connection()
    try:
        patient = auth_menu(conn, 'patient')
        if patient:
            portal = PatientPortal(patient)
            portal.display_menu()
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    finally:
        conn.close()