import datetime

class Person:
    def __init__(self, name, age, gender, person_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.person_id = person_id


class Doctor(Person):
    def __init__(self, name, age, gender, person_id, specialization):
        super().__init__(name, age, gender, person_id)
        self.specialization = specialization
        self.schedule = []
        self.patients_assigned = []


class Nurse(Person):
    def __init__(self, name, age, gender, person_id, assigned_ward, shift_time):
        super().__init__(name, age, gender, person_id)
        self.assigned_ward = assigned_ward
        self.shift_time = shift_time


class Patient(Person):
    def __init__(self, name, age, gender, person_id, symptoms):
        super().__init__(name, age, gender, person_id)
        self.symptoms = symptoms
        self.medical_history = []
        self.assigned_doctor = None


class Appointment:
    def __init__(self, appointment_id, doctor, patient, date_time):
        self.appointment_id = appointment_id
        self.doctor = doctor
        self.patient = patient
        self.datetime = date_time
        self.status = "Scheduled"

    def __str__(self):
        return f"ID: {self.appointment_id} | Dr. {self.doctor.name} with {self.patient.name} at {self.datetime} ({self.status})"


class MedicalRecord:
    def __init__(self, record_id, patient, diagnosis, prescription, doctor):
        self.record_id = record_id
        self.patient = patient
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.doctor = doctor
        self.date = datetime.date.today()

    def view_entry(self):
        return f"Date: {self.date} | Diagnosis: {self.diagnosis} | Rx: {self.prescription} | Dr. {self.doctor.name}"



class HospitalSystem:
    def __init__(self):
        self.patients = {}
        self.staff = {}  # Doctors and Nurses
        self.appointments = []
        self.records = []

    def add_person(self, person):
        if isinstance(person, (Doctor, Nurse)):
            self.staff[person.person_id] = person
        else:
            self.patients[person.person_id] = person

    def find_person(self, p_id):
        return self.staff.get(p_id) or self.patients.get(p_id)

    def create_appointment(self, doc_id, pat_id, time_str):
        doc = self.staff.get(doc_id)
        pat = self.patients.get(pat_id)
        if doc and pat:
            app_id = len(self.appointments) + 1
            new_app = Appointment(app_id, doc, pat, time_str)
            self.appointments.append(new_app)
            print("Appointment Booked!")
        else:
            print("Doctor or Patient ID invalid.")

    def log_medical_record(self, pat_id, doc_id, diagnosis, rx):
        pat = self.patients.get(pat_id)
        doc = self.staff.get(doc_id)
        if pat and doc:
            rec_id = len(self.records) + 1
            new_record = MedicalRecord(rec_id, pat, diagnosis, rx, doc)
            self.records.append(new_record)
            pat.medical_history.append(new_record)
            print("Record added to history.")



hospital = HospitalSystem()
hospital.add_person(Doctor("House", 45, "M", "D1", "Diagnostics"))
hospital.add_person(Patient("John Doe", 30, "M", "P1", "Flu"))


def main():
    while True:
        print("\n--- Hospital Login ---")
        print("1. Doctor\n2. Nurse (View only)\n3. Receptionist\n4. Patient\n5. Exit")
        role = input("Choice: ")

        if role == '3':  # Receptionist
            while True:
                print("\n(Receptionist Menu)\n1. Register Patient\n2. Book Appointment\n3. Assign Doctor\n4. Logout")
                choice = input("Action: ")
                if choice == '1':
                    name = input("Name: ")
                    p_id = input("ID: ")
                    sym = input("Symptoms: ")
                    hospital.add_person(Patient(name, 20, "N/A", p_id, sym))
                elif choice == '2':
                    d_id = input("Doctor ID: ")
                    p_id = input("Patient ID: ")
                    time = input("Time (e.g. 10:00 AM): ")
                    hospital.create_appointment(d_id, p_id, time)
                elif choice == '4':
                    break

        elif role == '1':  # Doctor
            doc_id = input("Enter your Doctor ID: ")
            doc = hospital.staff.get(doc_id)
            if not doc:
                print("Invalid ID");
                continue
            while True:
                print(
                    f"\nWelcome Dr. {doc.name}\n1. View Appointments\n2. Log Medical Record\n3. View Patient History\n4. Logout")
                choice = input("Action: ")
                if choice == '1':
                    for app in hospital.appointments:
                        if app.doctor.person_id == doc_id: print(app)
                elif choice == '2':
                    p_id = input("Patient ID: ")
                    diag = input("Diagnosis: ")
                    rx = input("Prescription: ")
                    hospital.log_medical_record(p_id, doc_id, diag, rx)
                elif choice == '3':
                    p_id = input("Patient ID: ")
                    pat = hospital.patients.get(p_id)
                    if pat:
                        for r in pat.medical_history: print(r.view_entry())
                elif choice == '4':
                    break

        elif role == '5':
            break


if __name__ == "__main__":
    main()