from colorama import Fore, init 

init(autoreset=True)

def manage_doctors(auth_system):
    """Doctor management menu"""
    while True:
        print(Fore.BLUE + "\n--- Doctor Management ---")
        print(Fore.YELLOW + "\n1. Add New Doctor")
        print(Fore.YELLOW  + "2. Delete Doctor")
        print(Fore.YELLOW  + "3. Update Credentials")
        print(Fore.YELLOW  + "4. List All Doctors")
        print(Fore.YELLOW  + "5. Back to Main Menu")
        
        choice = input(Fore.BLUE  +"\nChoose option (1-5): ")
        
        if choice == '1':
            email = input("Doctor email: ")
            name = input("Full name: ")
            password = input("password: ")
            print(auth_system.add_doctor(email, name, password))
            
        elif choice == '2':
            email = input("Doctor email to delete: ")
            print(auth_system.delete_doctor(email))
            
        elif choice == '3':
            email = input("Doctor email to update: ")
            new_pass = input("New password: ")
            print(auth_system.update_doctor_password(email, new_pass))
            
        elif choice == '4':
            auth_system.list_doctors()
            
        elif choice == '5':
            return  # Go back to main menu
        else:
            print(Fore.YELLOW + "Invalid choice!")