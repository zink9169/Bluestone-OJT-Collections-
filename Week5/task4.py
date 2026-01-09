from datetime import datetime
import pickle
class Person:
    def __init__(self, name, age, gender, person_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.person_id = person_id
#inheritance
class Doctor(Person):
    def __init__(self, name, age, gender, person_id, specialization):
        super().__init__(name, age, gender, person_id)
        self.specialization = specialization
        self.schedule = []  # list of appointments
        self.patients_assigned = []
#inheritance
class Nurse(Person):
    def __init__(self, name, age, gender, person_id, assigned_ward, shift_time):
        super().__init__(name, age, gender, person_id)
        self.assigned_ward = assigned_ward
        self.shift_time = shift_time
#inheritance
class Patient(Person):
    def __init__(self, name, age, gender, person_id, symptoms):
        super().__init__(name, age, gender, person_id)
        self.symptoms = symptoms
        self.medical_history = []
        self.assigned_doctor = None


#Encapsulation (Data + Method ကို စု)
class Appointment:
    def __init__(self, appointment_id, doctor, patient, date_time):
        self.appointment_id = appointment_id
        self.doctor = doctor
        self.patient = patient
        self.date_time = date_time
        self.status = "Scheduled"
    def add_entry(self):
        self.doctor.schedule.append(self)
        self.patient.medical_history.append(self)
    def view_history(self):
        print(
            f"Appointment {self.appointment_id}: Dr.{self.doctor.name} with {self.patient.name} at {self.date_time} Status: {self.status}")


#Encapsulation (Data + Method ကို စု)
class MedicalRecord:
    def __init__(self, record_id, patient, diagnosis, prescription, doctor, date):
        self.record_id = record_id
        self.patient = patient
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.doctor = doctor
        self.date = date
    def add_entry(self):
        self.patient.medical_history.append(self)

        #Polymorphism (Method တူ၊ Behavior မတူ)
        #Appointment → appointment history ပြ MedicalRecord → medical record ပြ
    def view_history(self):
        print(
            f"Record {self.record_id}: {self.patient.name} - Diagnosis: {self.diagnosis}, Prescription: {self.prescription}, Doctor: {self.doctor.name}, Date: {self.date}")



class HospitalSystem:
    def __init__(self):
        #HospitalSystem HAS-A patients, staff, appointments, records
        self.patients = {}
        self.staff = {}  # doctor and nurse
        self.appointments = {}
        self.records = {}

    def add_person(self, person):
        #Patient ဖြစ်ရင် patients, Doctor/Nurse ဖြစ်ရင် staff
        #polymorphism + isinstance()
        if isinstance(person, Patient):
            self.patients[person.person_id] = person
        else:
            self.staff[person.person_id] = person

    def find_person_by_id(self, person_id):
        #Code reuse
        return self.patients.get(person_id) or self.staff.get(person_id)

#object collaboration(doctor, patient, appointment)
    def create_appointment(self, appointment_id, doctor_id, patient_id, date_time):
        doctor = self.staff.get(doctor_id)
        patient = self.patients.get(patient_id)


        if doctor and patient:
            appointment = Appointment(appointment_id, doctor, patient, date_time)
            self.appointments[appointment_id] = appointment
            appointment.add_entry()
            print("Appointment created successfully!")
        else:
            print("Invalid doctor or patient ID.")

    def assign_doctor_to_patient(self, doctor_id, patient_id):
        doctor = self.staff.get(doctor_id)
        patient = self.patients.get(patient_id)
        if doctor and patient:
            #Doctor ↔ Patient relationship link
            patient.assigned_doctor = doctor
            doctor.patients_assigned.append(patient)
            print(f"Doctor {doctor.name} assigned to patient {patient.name}.")
        else:
            print("Invalid doctor or patient ID.")

#Doctor creates MedicalRecord for Patient
#Record auto-added to patient history
    def log_medical_record(self, record_id, patient_id, diagnosis, prescription, doctor_id):
        patient = self.patients.get(patient_id)
        doctor = self.staff.get(doctor_id)
        if patient and doctor:
            record = MedicalRecord(record_id, patient, diagnosis, prescription, doctor, datetime.now())
            self.records[record_id] = record
            record.add_entry()
            print("Medical record logged successfully!")
        else:
            print("Invalid patient or doctor ID.")

    def view_all_appointments(self):
        for app in self.appointments.values():
            app.view_history()

    def save_data(self, filename='hospital_data.pkl'):
        with open(filename, 'wb') as f:
            #HospitalSystem object တစ်ခုလုံးကို file ထဲသိမ်း
            pickle.dump(self, f)

    # Static Method  → "General purpose tool"
    # Normal Method  → "Tool attached to this specific object"
    @staticmethod
    def load_data(filename='hospital_data.pkl'):
        try:
            with open(filename, 'rb') as f:
                #System state ကို ပြန်လည်ဖတ်ယူ
                return pickle.load(f)
        except:
            return HospitalSystem()


def main_menu():
    hospital = HospitalSystem.load_data()

    while True:
        print("Hospital Management System")
        print("Please log in as:")
        print("1. Doctor")
        print("2. Nurse")
        print("3. Receptionist")
        print("4. Patient")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            doctor_menu(hospital)
        elif choice == '2':
            print("Nurse menu not implemented yet.")
        elif choice == '3':
            receptionist_menu(hospital)
        elif choice == '4':
            print("Patient menu not implemented yet.")
        elif choice == '5':
            hospital.save_data()
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice!")


def doctor_menu(hospital):
    doctor_id = input("Enter your Doctor ID: ")
    doctor = hospital.staff.get(doctor_id)
    if not isinstance(doctor, Doctor):
        print("Invalid Doctor ID!")
        return

    while True:
        print("Doctor Menu ({doctor.name})")
        print("1. View Appointments")
        print("2. Log Medical Record")
        print("3. View Patient History")
        print("4. Back to Main Menu")
        choice = input("Enter choice: ")

        if choice == '1':
            for app in doctor.schedule:
                app.view_history()
        elif choice == '2':
            patient_id = input("Patient ID: ")
            diagnosis = input("Diagnosis: ")
            prescription = input("Prescription: ")
            record_id = f"R{len(hospital.records) + 1:03d}"
            hospital.log_medical_record(record_id, patient_id, diagnosis, prescription, doctor_id)
        elif choice == '3':
            patient_id = input("Patient ID: ")
            patient = hospital.patients.get(patient_id)
            if patient:
                for record in patient.medical_history:
                    if isinstance(record, MedicalRecord):
                        record.view_history()
            else:
                print("Invalid Patient ID!")
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

def receptionist_menu(hospital):
    while True:
        print("Receptionist Menu")
        print("1. Register Patient")
        print("2. Book Appointment")
        print("3. Assign Doctor")
        print("4. Cancel Appointment")
        print("5. Back to Main Menu")
        choice = input("Enter choice: ")

        if choice == '1':
            pid = input("Patient ID: ")
            name = input("Name: ")
            age = int(input("Age: "))
            gender = input("Gender: ")
            symptoms = input("Symptoms: ")
            patient = Patient(name, age, gender, pid, symptoms)
            hospital.add_person(patient)
            print("Patient registered successfully!")
        elif choice == '2':
            app_id = input("Appointment ID: ")
            doctor_id = input("Doctor ID: ")
            patient_id = input("Patient ID: ")
            dt = input("Date & Time (YYYY-MM-DD HH:MM): ")
            hospital.create_appointment(app_id, doctor_id, patient_id, dt)
        elif choice == '3':
            doctor_id = input("Doctor ID: ")
            patient_id = input("Patient ID: ")
            hospital.assign_doctor_to_patient(doctor_id, patient_id)
        elif choice == '4':
            app_id = input("Appointment ID to cancel: ")
            if app_id in hospital.appointments:
                app = hospital.appointments.pop(app_id)
                app.status = "Cancelled"
                print("Appointment cancelled.")
            else:
                print("Invalid Appointment ID.")
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()
# Receptionist → create Appointment
# Doctor → logs Medical Record
# Patient → medical_history updated
# HospitalSystem → manages all