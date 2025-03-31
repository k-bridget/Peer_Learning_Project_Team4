def view_help_requests(auth_system):
    print("\n--- Help Requests ---")
    requests = auth_system.get_all_help_requests()
    
    if not requests:
        print("No help requests found.")
        return
    
    for req in requests:
        print(f"\nID: {req[0]}")
        print(f"User: {req[1]}")
        print(f"Time: {req[3]}")
        print(f"Message: {req[2]}")
        print("-" * 30)

def get_request(auth_system):
    view_help_requests(auth_system)
    
    print()
    print("1. Back")
    while True:
        choice = input("\nChoose option (1): ")
        if choice == '1':
            break
        print("Invalid choice. Try again.")