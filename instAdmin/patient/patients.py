def view_appointments(auth_system):
    """Display appointments in minimal format"""
    print("\n--- Appointment Records ---")
    appoints = auth_system.get_all_appointments()
    
    if not appoints:
        print("No appointments found.")
        return
    
    print("\nAll Appointments:")
    for appt in appoints:
        print(f"User: {appt[0]} | Appointment ID: {appt[1]} | Time: {appt[2]}")
