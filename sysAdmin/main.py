import sys
from pathlib import Path
from colorama import Fore, init 


# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent))
init(autoreset=True)

from monitor.sysmonitor import monitoring
from helpreq.request import get_request
from recovered.recovered import recovered_menu

def sys_menu(auth_system):
 
    while True:
        print(Fore.MAGENTA + r'''
         _____            _____   _       _     
        |   __|_ _ ___   |  _  |_| |_____|_|___ 
        |__   | | |_ -|  |     | . |     | |   |
        |_____|_  |___|  |__|__|___|_|_|_|_|_|_|
              |___|                            
      ''')
        print(Fore.BLUE + "\nWelcome to System Admin Portal")
        print(Fore.YELLOW + "\n1. System Monitoring")
        print(Fore.YELLOW + "2. Help Request")
        print(Fore.YELLOW + "3. Password Recovered")
        print(Fore.YELLOW + "4. Logout")
        choice = input("\nYour choice >>>  ")

        if choice == '1':
            monitoring()
        elif choice == '2':
            get_request(auth_system)
        elif choice == '3':
            recovered_menu(auth_system)
        elif choice == '4':
            print("Logging out....")
            break
        else:
            print("Invalid input.")