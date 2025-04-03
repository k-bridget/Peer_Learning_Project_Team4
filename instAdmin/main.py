import sys
from pathlib import Path
from colorama import Fore, init 

init(autoreset=True)
sys.path.append(str(Path(__file__).parent))

import mysql.connector
from mysql.connector import Error

# Importing the features
from affili.affiliate import manage_doctors
from patient.patients import view_appointments
from rating.ratings import view_performance_ratings

    
def init_menu(auth_system):
    while True:
        print(Fore.MAGENTA + r'''
         _         _      _____   _       _     
        |_|___ ___| |_   |  _  |_| |_____|_|___ 
        | |   |_ -|  _|  |     | . |     | |   |
        |_|_|_|___|_|    |__|__|___|_|_|_|_|_|_|
        ''')   
        print(Fore.BLUE + "\nWelcome to Institutional Management Portal")
        print(Fore.YELLOW + "\n1. Affiliated Workers Management")
        print(Fore.YELLOW + "2. Institutional Performance Dashboard")
        print(Fore.YELLOW + "3. Patient Appointments Overview")
        print(Fore.YELLOW + "4. Logout")
        
        choice = input("\nYour choice >>> ")

        if choice == '1':
            manage_doctors(auth_system)
        elif choice == '2':
            view_performance_ratings(auth_system)
        elif choice == '3':
            view_appointments(auth_system)
        elif choice == '4':
            print("\nLogging out...")
            break
        else:
            print(Fore.RED + "\nInvalid input. Please choose 1-4.")

if __name__ == "__main__":
    auth = AuthSystem(
        host="localhost",
        user="root",
        password="school",
        database="mindsafe"
    )
    init_menu(auth)