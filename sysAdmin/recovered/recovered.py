from colorama import Fore, init 

init(autoreset=True)

def view_recovery_history(AuthSystem):
    """Display recovery records in simple list format"""
    print(Fore.BLUE + "\n--- Password Recovery History ---")
    records = AuthSystem.get_recovery_records()
    
    if not records:
        print(Fore.BLUE + "No recovery records found.")
        return
    
    print(Fore.BLUE + "\nRecovery Records:")
    for record in records:
        print(f"ID: {record[0]} | Email: {record[1]} | Time: {record[2]}")

def recovered_menu(AuthSystem):   
    view_recovery_history(AuthSystem)
    
    print()
    print(Fore.YELLOW + "1. Back to Main Menu")
    while True:
        choice = input(Fore.BLUE + "\nChoose option (1): ")
        if choice == '1':
            break
        print(Fore.RED + "Invalid choice. Try again.")
        