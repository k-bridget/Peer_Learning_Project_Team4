def view_recovery_history(AuthSystem):
    """Display recovery records in simple list format"""
    print("\n--- Password Recovery History ---")
    records = AuthSystem.get_recovery_records()
    
    if not records:
        print("No recovery records found.")
        return
    
    print("\nRecovery Records:")
    for record in records:
        print(f"ID: {record[0]} | Email: {record[1]} | Time: {record[2]}")

def recovered_menu(AuthSystem):   
    view_recovery_history(AuthSystem)
    
    print()
    print("1. Back to Main Menu")
    while True:
        choice = input("\nChoose option (1)")
        if choice == '1':
            break
        print("Invalid choice. Try again.")