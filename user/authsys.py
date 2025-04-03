from colorama import Fore, init
from getpass import getpass
import mysql.connector

init(autoreset=True)

class auth:
    def __init__(self, conn):
        self.conn = conn
    
    def login(self, user_id, password):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Users WHERE user_id = %s AND password = %s",
                (user_id, password))
            return cursor.fetchone()
        finally:
            cursor.close()

    def signup(self, user_id, password, security_questions):
        cursor = self.conn.cursor()
        try:
            # Insert user
            cursor.execute(
                "INSERT INTO Users (user_id, password) VALUES (%s, %s)",
                (user_id, password))
            
            # Insert security questions
            for q, a in security_questions:
                cursor.execute(
                    """INSERT INTO Security_Questions (user_id, question, answer)
                    VALUES (%s, %s, %s)""",
                    (user_id, q, a))
            
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(Fore.RED + f"Error: {err}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def reset_password(self, user_id, new_password):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE Users SET password = %s WHERE user_id = %s",
                (new_password, user_id))
            self.conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def get_security_questions(self, user_id):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT question, answer FROM Security_Questions WHERE user_id = %s",
                (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

def auth_menu(conn, user_type='patient'):
    auth = auth(conn)
    while True:
        print(Fore.CYAN + f"\n{user_type.title()} Authentication")
        print(Fore.YELLOW + "1. Login")
        print(Fore.YELLOW + "2. Sign Up")
        print(Fore.YELLOW + "3. Forgot Password")
        print(Fore.YELLOW + "4. Back")
        
        choice = input(Fore.WHITE + "Choose option: ")

        if choice == '1':
            user = handle_login(auth)
            if user:
                return user
        elif choice == '2':
            handle_signup(auth)
        elif choice == '3':
            handle_password_reset(auth)
        elif choice == '4':
            return None
        else:
            print(Fore.RED + "Invalid choice!")

def handle_login(auth):
    print(Fore.CYAN + "\nLogin")
    user_id = input("User ID: ")
    password = getpass("Password: ")
    
    user = auth.login(user_id, password)
    if user:
        print(Fore.GREEN + "Login successful!")
        return user
    print(Fore.RED + "Invalid credentials!")
    return None

def handle_signup(auth):
    print(Fore.CYAN + "\nSign Up")
    user_id = input("Choose user ID: ")
    password = getpass("Choose password: ")
    
    print(Fore.YELLOW + "\nSet up security questions:")
    questions = [
        (input("Question 1: "), getpass("Answer 1: ")),
        (input("Question 2: "), getpass("Answer 2: ")),
        (input("Question 3: "), getpass("Answer 3: "))
    ]
    
    if auth.signup(user_id, password, questions):
        print(Fore.GREEN + "\nRegistration successful! Please login.")
    else:
        print(Fore.RED + "\nRegistration failed!")

def handle_password_reset(auth):
    print(Fore.CYAN + "\nPassword Reset")
    user_id = input("Enter your user ID: ")
    
    questions = auth.get_security_questions(user_id)
    if not questions:
        print(Fore.RED + "No security questions found!")
        return
    
    print(Fore.YELLOW + "\nAnswer security questions:")
    for i, q in enumerate(questions, 1):
        answer = getpass(f"{i}. {q['question']}: ")
        if answer != q['answer']:
            print(Fore.RED + "Incorrect answers!")
            return
    
    new_password = getpass("New password: ")
    confirm_password = getpass("Confirm password: ")
    
    if new_password == confirm_password:
        if auth.reset_password(user_id, new_password):
            print(Fore.GREEN + "Password reset successfully!")
        else:
            print(Fore.RED + "Password reset failed!")
    else:
        print(Fore.RED + "Passwords do not match!")