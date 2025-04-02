<div align='center'> 
<h1> MindSafe 🧠</h1>
</div>
In many regions, mental health patients face significant barriers to accessing professional care, such as stigma, limited availability of mental health professionals, being judged, and a lack of anonymity. These obstacles can discourage patients from seeking the help they need, which may lead to untreated mental health conditions, a worsening of symptoms, and decreased quality of life. On the other hand, healthcare providers, particularly mental health professionals, may struggle to connect with patients who are reluctant to share their struggles due to fears of judgment or confidentiality concerns.

## Our Why
In an age where confidentiality is key, Mindsafe aims to create a platform where mental health patients can communicate with doctors anonymously, ensuring privacy and a high standard of security at every stage of the interaction, providing a safe and secure environment for individuals seeking mental health support by connecting them with qualified professionals.By eliminating barriers such as the fear of being judged, we aim to make mental health support more accessible and confidential for those in need.

## Our Prototype
### Features

- Booking session
- Authentication
- System monitoring
- Help request functionality
- Workers management
- Password recovery

### How it works

##### Authentication
The part where we will have all built-in methods defined in the main auth system class so that whenever the user chooses the patient, doctor, system admin, or institutional admin, we can call that built-in method to serve him/her.

The patient and institutional admin will only have login, signup, forgot password, and exit options. Doctors will only have login and exit options; for system admin, we will only have login and exit options.  

- *Login*: after asking him/her the email(primary key) and password and it matches with the ones in the database, we will switch to the function from another file in the working directory and return his credentials in a dictionary so that we can use it while he/she will be in the system.

- *Signup*: we will ask him/her the user name he/she will be using in booking and whatever, the email which will act as the primary key, three questions that will be used during the recovery process, gender(Male, Female, LGBT)so that we can use that to offer personalized services.

- *Forgot password*: we will acquire the user's email so that we can check if it's in a database or not; if it's in the database, we will prompt the user with the recovery questions, and if all matches, we will show the password and then give him/her option to change password or go back to the login menu.

- *Exit*: we will go to the home menu.
  
##### Booking Session

##### Password Recovery

##### System Monitoring

### Our Users 👨‍👩‍👦‍👦 
##### 1. Doctors 👨‍⚕️
Flow logic is where he/she'll have bookings, my profile, my blog, and logout options.

- *Bookings*: he/she must have options to upload a session where he will put the link of Google Meet so that we can offer that to our patient, setting the starting time and the ending time so that the user, by the time to book, will know how it is, and other option to know what booked and by who(to mean the user/patient), another option to get the reminders of the upcoming events basing on the nearest. and he/she must specify the gender the sessions are for.

- *My Profile*: he/she will be able to manage his/her biography and what he/she is an expert in with options to update or go back to the main menu.

- *My Blog*: he/she will be able to write quick tips that will be seen on the patient dashboard with options to write a new blog, update an existing one based on ID (which must be auto-incremented), or delete some blog. and for a cool way, we will get these blogs and display them in the main menu of the user(like after 50 seconds, and keep that space for blogs while one ends, another continues without taking another place), and the last option to go back to the main menu.

- *Logout*: he/she will log out to the home without returning to the authentication logic.

##### 2. Patient 👨‍👩‍👧‍👦
Flow logic is where he/she'll have appointments, my profile, help, rating, and logout options.
- *Appointments*: he/she will be able to book available sessions with the doctor with options of book new appointments, view upcoming appointments(means those that are not taken by others), Reminders(for upcoming sessions), and go back to the main menu options.
  
- *My Profile*: he/she'll be able to check his/her name, email, and all his credentials that are visible to others and back to the main menu option.
  
- *Help*: he/she will write the new help request with a message and his/her user_id that will update the help_request table and then be able to be viewed by the system admin.
  
- *Rating*: he/she'll be able to rate the sessions done with relative doctors out of 10.so that it'll be viewed by the institutional admin to track the performance of his/her institution.
  
- *Logout*: he/she will log out to the home without returning to the authentication logic.

##### 3. System Admin ⛑️
Flow logic is where system admins will have system monitoring, help requests, password recovery, and exit options.
- *System Monitoring*: Where he/she will know the health of the system from CPU health up to Disk memory and warn us based on the threshold.
  
- *Help Request*: Where the system admin will be able to get the request from the user(patient) and be able to know what to improve.
  
-  *Password Recovered*: Just all the logs about the password recovered and by whom.
  
- *Logout*: he/she will log out to the home without returning to the authentication logic.

##### 4. Institutional Admin 👨‍⚕️
The flow was the Affiliated worker's management, institutional performance, patient appointments overview, and logout options.
- *Affiliated Worker's Management*: This has management features like adding doctors, deleting doctors, updating doctors' credentials, and checking the list of all doctors.
  
- *Institutional Performance*: Where the institutional admin will be checking the ratings of their doctors/therapists in general.
  
- * Patient Appointments Overview*: Where institutional admin will check logs about how the patients booked sessions with their doctors/therapist.
  
- *Logout*: he/she will log out to the home without returning to the authentication logic.
  
### Setup 🧰

---
## Screenshots:

## Contributions:





