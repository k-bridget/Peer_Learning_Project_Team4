# MindSafe User Experience Flow
portals = {
    "patient": {},
    "doctor": {},
    "admin": {},
    "sysadmin": {"admin": "adminpass"}  # Sys Admin's credentials for logging in
}
doctor_appointments = {
    "Dr. Nathanaella": [],
    "Dr. Kingly": [],
    "Dr. Bridget": [],
    "Dr. Faith": []
}

def show_welcome():
    print("Welcome to MindSafe!")
    print("1. Sign Up")
    print("2. Log In")
    print("3. Exit")

def sign_up(role):
    anonymous_name = input(f"Create an anonymous name for {role}: ")
    print(f"{role.capitalize()} sign-up successful. Welcome, {anonymous_name}!")
    return anonymous_name

def log_in(role):
    anonymous_name = input(f"Enter your anonymous name for {role}: ")
    print(f"Welcome back, {anonymous_name}!")
    return anonymous_name

def get_role_input():
    while True:
        role = input("Enter your role (patient, doctor, admin, sysadmin): ").lower()
        if role in portals:
            return role
        else:
            print("Invalid role! Please enter a valid role: patient, doctor, admin, or sysadmin.")

def select_support_type():
    print("Please select the type of support you need:")
    print("1. Anxiety")
    print("2. Depression")
    print("3. General Well-being")
    print("4. Any other support type.")
    support_type = input("Enter the number of your choice: ")

    while support_type not in ['1', '2', '3', '4']:
        print("Invalid choice. Please select a valid support type.")
        support_type = input("Enter the number of your choice: ")

    if support_type == '1':
        print("You selected Anxiety support.")
    elif support_type == '2':
        print("You selected Depression support.")
    elif support_type == '3':
        print("You selected General Well-being support.")
    elif support_type == '4':
        print("You selected any other support type")
    return support_type

def browse_doctors():
    print("Here are the available anonymous doctors for your selected support type:")
    print("1. Dr. Nathanaella (Anxiety Specialist)")
    print("2. Dr. Kingly (Depression Specialist)")
    print("3. Dr. Bridget (General Well-being Specialist)")
    print("4. Dr. Faith (Mental health specialist)")

    doctor_choice = input("Enter the number of your preferred doctor: ")

    while doctor_choice not in ['1', '2', '3', '4']:
        print("Invalid choice. Please select a valid doctor.")
        doctor_choice = input("Enter the number of your preferred doctor: ")

    doctor_dict = {
        '1': 'Dr. Nathanaella',
        '2': 'Dr. Kingly',
        '3': 'Dr. Bridget',
        '4': 'Dr. Faith'
    }
    
    return doctor_dict[doctor_choice]

def book_appointment(doctor_name, patient_name):
    print(f"Select an available time slot for {doctor_name}:")
    print("1. 10:00 AM")
    print("2. 2:00 PM")
    print("3. 5:00 PM")
    print("4. 8:00 AM")
    time_slot = input("Enter the number of your choice: ")

    while time_slot not in ['1', '2', '3', '4']:
        print("Invalid choice. Please select a valid time slot.")
        time_slot = input("Enter the number of your choice: ")

    # Convert time slot number to actual time for display
    time_dict = {
        '1': '10:00 AM',
        '2': '2:00 PM',
        '3': '5:00 PM',
        '4': '8:00 AM'
    }
    actual_time = time_dict[time_slot]

    print(f"Your appointment with {doctor_name} is booked for {actual_time}.")
    
    # Store the appointment in the doctor_appointments dictionary
    doctor_appointments[doctor_name].append({
        "patient_name": patient_name,
        "time_slot": actual_time
    })
    return actual_time

def patient_flow():
    print("Patient Flow")
    support_type = select_support_type()
    doctor_name = browse_doctors()  
    patient_name = input("Enter your anonymous name: ")  
    time_slot = book_appointment(doctor_name, patient_name) 

def doctor_flow():
    print("Doctor Flow")
    print("You can now view patient requests and manage your availability.")
    print("1. View Patient Requests")
    print("2. View Consultation Notes")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")

    # Validate the doctor's choice
    while choice not in ['1', '2', '3']:
        print("Invalid choice. Please select a valid option.")
        choice = input("Enter your choice (1-3): ")

    if choice == '1':
        # Show the list of patients who have scheduled appointments with this doctor
        print("Viewing Patient Requests...")
        for doctor, appointments in doctor_appointments.items():
            if doctor == "Dr. Nathanaella":
                print(f"Appointments for {doctor}:")
                for appointment in appointments:
                    print(f"Patient: {appointment['patient_name']} - Appointment Time: {appointment['time_slot']}")
            elif doctor == "Dr. Kingly":
                print(f"Appointments for {doctor}:")
                for appointment in appointments:
                    print(f"Patient: {appointment['patient_name']} - Appointment Time: {appointment['time_slot']}")
            elif doctor == "Dr. Bridget":
                print(f"Appointments for {doctor}:")
                for appointment in appointments:
                    print(f"Patient: {appointment['patient_name']} - Appointment Time: {appointment['time_slot']}")
            elif doctor == "Dr. Faith":
                print(f"Appointments for {doctor}:")
                for appointment in appointments:
                    print(f"Patient: {appointment['patient_name']} - Appointment Time: {appointment['time_slot']}")
    elif choice == '2':
        print("Viewing Consultation Notes...")
    elif choice == '3':
        print("Exiting...")

def institutional_admin_flow():
    print("Institutional Admin Flow")
    print("1. Manage Doctor Profiles")
    print("2. Monitor Consultations")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")

    while choice not in ['1', '2', '3']:
        print("Invalid choice. Please select a valid option.")
        choice = input("Enter your choice (1-3): ")

    if choice == '1':
        print("Managing Doctor Profiles...")
    elif choice == '2':
        print("Monitoring Consultations...")
    elif choice == '3':
        print("Exiting...")

def sys_admin_flow():
    print("System Admin Flow")
    print("1. Manage Users (Doctors, Admins)")
    print("2. View System Logs")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")

    while choice not in ['1', '2', '3']:
        print("Invalid choice. Please select a valid option.")
        choice = input("Enter your choice (1-3): ")

    if choice == '1':
        print("Managing users (Doctors, Admins)...")
    elif choice == '2':
        print("Viewing System Logs...")
    elif choice == '3':
        print("Exiting...")

# Main function to run the flow
def main():
    while True:
        show_welcome()
        choice = input("Enter your choice (1-3): ")

        while choice not in ['1', '2', '3']:
            print("Invalid choice. Please select a valid option.")
            choice = input("Enter your choice (1-3): ")

        if choice == '1':  # Sign up
            role = get_role_input()
            anonymous_name = sign_up(role)
            portals[role][anonymous_name] = role  # Save anonymous_name with role
            print(f"{role.capitalize()} signed up successfully as {anonymous_name}")
            if role == "patient":
                patient_flow()
        elif choice == '2':  # Log in
            role = get_role_input()
            anonymous_name = log_in(role)
            if anonymous_name in portals[role]:
                print(f"Logged in as {anonymous_name}")
                if role == "patient":
                    patient_flow()
                elif role == "doctor":
                    doctor_flow()
                elif role == "admin":
                    institutional_admin_flow()
                elif role == "sysadmin":
                    sys_admin_flow()
            else:
                print("Invalid pseudonym. Please try again.")
        elif choice == '3':  # Exit
            print("Exiting the application. Take care!")
            break

# Run the program
main()


