import random

class Doctor:
    def __init__(self, specialty, availability, rating=5.0, feedback_count=0):
        self.specialty = specialty
        self.availability = availability  # List of available time slots
        self.rating = rating  # Average rating
        self.feedback_count = feedback_count  # Number of feedback received
    
    def update_rating(self, new_rating):
        """Update the doctor's rating based on new feedback."""
        total_score = self.rating * self.feedback_count + new_rating
        self.feedback_count += 1
        self.rating = total_score / self.feedback_count
    
    def __repr__(self):
        return f"{self.specialty} (Rating: {self.rating:.2f})"

class MatchingSystem:
    def __init__(self):
        self.doctors = []
    
    def add_doctor(self, doctor):
        self.doctors.append(doctor)
    
    def match_patient(self, specialty_request):
        """Match a patient to the best available doctor based on specialty and rating."""
        matching_doctors = [doc for doc in self.doctors if doc.specialty.lower() == specialty_request.lower()]
        
        if not matching_doctors:
            return "No available doctors for this specialty."
        
        # Sort doctors by rating (higher is better) and then by availability (more slots available is better)
        matching_doctors.sort(key=lambda d: (-d.rating, -len(d.availability)))
        
        return matching_doctors[0]  # Best doctor match
    
    def provide_feedback(self, specialty, rating):
        """Allow patients to provide feedback and update doctor rating."""
        for doc in self.doctors:
            if doc.specialty == specialty:
                doc.update_rating(rating)
                return f"Feedback recorded. {doc.specialty}'s new rating: {doc.rating:.2f}"
        return "Doctor not found."

def main():
    matching_system = MatchingSystem()

    # Adding doctors
    d1 = Doctor("Therapy", ["Monday", "Wednesday"], 4.5, 10)
    d2 = Doctor("Therapy", ["Tuesday", "Thursday"], 4.8, 20)
    d3 = Doctor("General Medicine", ["Monday", "Friday"], 4.2, 15)

    matching_system.add_doctor(d1)
    matching_system.add_doctor(d2)
    matching_system.add_doctor(d3)

    # Matching a patient
    print(matching_system.match_patient("Therapy"))

    # Providing feedback
    print(matching_system.provide_feedback("Therapy", 5))

if __name__ == "__main__":
    main()
