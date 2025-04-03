import mysql.connector
import threading
import time

from colorama import Fore, Style, init
from datetime import datetime
from getpass import getpass

init(autoreset=True)  # Initialize Colorama

# Database Configuration
def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="school",
        database="mindsafe"
    )
class DoctorPortal:
    def __init__(self, doctor_data):
        self.doctor = doctor_data
        self.conn = create_db_connection()
        self.blog_running = True
        
    def display_menu(self):
        while True:
            print(Fore.MAGENTA + r'''
             ____                       _       _ 
            |    \ ___      ___ ___ ___| |_ ___| |
            |  |  |  _|_   | . | . |  _|  _| .'| |
            |____/|_| |_|  |  _|___|_| |_| |__,|_|
                           |_|                    
            ''')
            print(Fore.BLUE + "\nDoctor's Portal Dashboard")
            print(Fore.YELLOW + "\n1. Manage Bookings")
            print(Fore.YELLOW + "2. My Profile")
            print(Fore.YELLOW + "3. My Blog")
            print(Fore.YELLOW + "4. Logout")
            
            choice = input(Fore.WHITE + "Your choice >>> ")

            if choice == '1':
                self.manage_bookings()
            elif choice == '2':
                self.manage_profile()
            elif choice == '3':
                self.manage_blog()
            elif choice == '4':
                self.blog_running = False
                self.conn.close()
                print(Fore.GREEN + "Logging out....")
                break
            else:
                print(Fore.RED + "Invalid input. Please try again.")

    def manage_bookings(self):
        while True:
            print(Fore.CYAN + "\nBookings Management")
            print(Fore.YELLOW + "\n1. Create New Session")
            print(Fore.YELLOW + "2. View Booked Sessions")
            print(Fore.YELLOW + "3. View Upcoming Reminders")
            print(Fore.YELLOW + "4. Back to Main Menu")
            
            choice = input(Fore.WHITE + "Your choice >>> ")
            
            if choice == '1':
                self.create_session()
            elif choice == '2':
                self.view_bookings()
            elif choice == '3':
                self.view_reminders()
            elif choice == '4':
                break
            else:
                print(Fore.RED + "Invalid choice!")

    def create_session(self):
        try:
            print(Fore.CYAN + "\nCreate New Session")
            meet_link = input("Google Meet Link: ")
            start_time = input("Start Time (YYYY-MM-DD HH:MM): ")
            end_time = input("End Time (YYYY-MM-DD HH:MM): ")
            gender = input("Gender (Male/Female/Any): ").capitalize()

            cursor = self.conn.cursor()
            query = """INSERT INTO doctor_sessions 
                     (doctor_id, meet_link, start_time, end_time, gender)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                self.doctor['doctor_id'],
                meet_link,
                start_time,
                end_time,
                gender
            ))
            self.conn.commit()
            print(Fore.GREEN + "Session created successfully!")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def view_bookings(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """SELECT a.appointment_id, a.user_id, a.timestamp, 
                      ds.meet_link, ds.start_time 
                      FROM appointments a
                      JOIN doctor_sessions ds ON a.session_id = ds.session_id
                      WHERE ds.doctor_id = %s"""
            cursor.execute(query, (self.doctor['doctor_id'],))
            bookings = cursor.fetchall()
            
            if not bookings:
                print(Fore.YELLOW + "\nNo current bookings")
                return
                
            print(Fore.CYAN + "\nCurrent Bookings:")
            for book in bookings:
                print(f"\nID: {book['appointment_id']}")
                print(f"Patient: {book['user_id']}")
                print(f"Session Time: {book['start_time']}")
                print(f"Meet Link: {book['meet_link']}")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def view_reminders(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """SELECT * FROM doctor_sessions 
                     WHERE doctor_id = %s AND start_time > NOW()
                     ORDER BY start_time LIMIT 5"""
            cursor.execute(query, (self.doctor['doctor_id'],))
            sessions = cursor.fetchall()
            
            if not sessions:
                print(Fore.YELLOW + "\nNo upcoming sessions")
                return
                
            print(Fore.CYAN + "\nUpcoming Sessions:")
            for session in sessions:
                print(f"\nSession ID: {session['session_id']}")
                print(f"Time: {session['start_time']} to {session['end_time']}")
                print(f"Meet Link: {session['meet_link']}")
                print(f"Gender: {session['gender']}")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def manage_profile(self):
        while True:
            print(Fore.CYAN + "\nProfile Management")
            print(Fore.YELLOW + "\n1. View Profile")
            print(Fore.YELLOW + "2. Update Biography")
            print(Fore.YELLOW + "3. Update Expertise")
            print(Fore.YELLOW + "4. Back to Main Menu")
            
            choice = input(Fore.WHITE + "\nYour choice >>> ")
            
            if choice == '1':
                self.view_profile()
            elif choice == '2':
                self.update_profile_field('biography')
            elif choice == '3':
                self.update_profile_field('expertise')
            elif choice == '4':
                break
            else:
                print(Fore.RED + "Invalid choice!")

    def view_profile(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", 
                          (self.doctor['doctor_id'],))
            profile = cursor.fetchone()
            
            print(Fore.CYAN + "\nYour Profile:")
            print(f"Name: {profile['name']}")
            print(f"Email: {profile['email']}")
            print(f"\nBiography:\n{profile['biography']}")
            print(f"\nExpertise: {profile['expertise']}")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def update_profile_field(self, field):
        try:
            new_value = input(f"Enter new {field}: ")
            cursor = self.conn.cursor()
            query = f"UPDATE doctors SET {field} = %s WHERE doctor_id = %s"
            cursor.execute(query, (new_value, self.doctor['doctor_id']))
            self.conn.commit()
            print(Fore.GREEN + "Profile updated successfully!")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def manage_blog(self):
        while True:
            print(Fore.CYAN + "\nBlog Management")
            print(Fore.YELLOW + "\n1. Write New Blog")
            print(Fore.YELLOW + "2. Update Existing Blog")
            print(Fore.YELLOW + "3. Delete Blog")
            print(Fore.YELLOW + "4. Back to Main Menu")
            
            choice = input(Fore.WHITE + "\nYour choice >>> ")
            
            if choice == '1':
                self.create_blog()
            elif choice == '2':
                self.update_blog()
            elif choice == '3':
                self.delete_blog()
            elif choice == '4':
                break
            else:
                print(Fore.RED + "Invalid choice!")

    def create_blog(self):
        try:
            content = input("Enter blog content: ")
            cursor = self.conn.cursor()
            query = """INSERT INTO blogs (doctor_id, content)
                     VALUES (%s, %s)"""
            cursor.execute(query, (self.doctor['doctor_id'], content))
            self.conn.commit()
            print(Fore.GREEN + "Blog post created successfully!")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def update_blog(self):
        try:
            blog_id = input("Enter blog ID to update: ")
            new_content = input("Enter new content: ")
            
            cursor = self.conn.cursor()
            query = """UPDATE blogs SET content = %s 
                     WHERE blog_id = %s AND doctor_id = %s"""
            cursor.execute(query, (new_content, blog_id, self.doctor['doctor_id']))
            self.conn.commit()
            
            if cursor.rowcount > 0:
                print(Fore.GREEN + "Blog updated successfully!")
            else:
                print(Fore.RED + "No blog found with that ID")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def delete_blog(self):
        try:
            blog_id = input("Enter blog ID to delete: ")
            
            cursor = self.conn.cursor()
            query = "DELETE FROM blogs WHERE blog_id = %s AND doctor_id = %s"
            cursor.execute(query, (blog_id, self.doctor['doctor_id']))
            self.conn.commit()
            
            if cursor.rowcount > 0:
                print(Fore.GREEN + "Blog deleted successfully!")
            else:
                print(Fore.RED + "No blog found with that ID")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
        finally:
            cursor.close()

    def display_blogs(self):
        while self.blog_running:
            try:
                cursor = self.conn.cursor(dictionary=True)
                query = """SELECT content FROM blogs 
                         WHERE doctor_id = %s 
                         ORDER BY created_at DESC LIMIT 1"""
                cursor.execute(query, (self.doctor['doctor_id'],))
                blog = cursor.fetchone()
                
                if blog:
                    print(Fore.MAGENTA + "\nLatest Health Tip:" + Style.RESET_ALL)
                    print(blog['content'] + "\n")
                
                time.sleep(50)
            except Exception as e:
                print(Fore.RED + f"Blog display error: {str(e)}")
            finally:
                cursor.close()

def handle_doctor_login():
    conn = create_db_connection()
    try:
        print(Fore.CYAN + "\nDoctor Login")
        email = input("Email: ")
        password = getpass("Password: ")
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctors WHERE email = %s AND password = %s", 
                    (email, password))
        doctor = cursor.fetchone()
        
        if doctor:
            portal = DoctorPortal(doctor)
            portal.display_menu()
    
        else:
            print(Fore.RED + "Invalid credentials!")
    except Exception as e:
        print(Fore.RED + f"Login error: {str(e)}")
    finally:
        conn.close()