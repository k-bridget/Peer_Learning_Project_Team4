from colorama import Fore, init 
init(autoreset=True)

def view_help_requests(auth_system):
    print(Fore.BLUE +"\n--- Help Requests ---")
    requests = auth_system.get_all_help_requests()
    
    if not requests:
        print(Fore.BLUE + "No help requests found.")
        return
    
    for req in requests:
        print(Fore.BLUE + f"\nID: {req[0]}")
        print(f"User: {req[1]}")
        print(f"Time: {req[3]}")
        print(f"Message: {req[2]}")
        print(Fore.Yellow + "-" * 30)

def get_request(auth_system):
    view_help_requests(auth_system)
    
    print()
    print(Fore.YELLOW + "1. Back to Main Menu")
    while True:
        choice = input(Fore.BLUE + "\nChoose option (1): ")
        if choice == '1':
            break
        print(Fore.RED + "Invalid choice. Try again.")
        