from datetime import datetime

class Person:
    def __init__(self, person_id, name, age, gender):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.gender = gender

class Doctor(Person):
    def __init__(self, person_id, name, age, gender, specialization):
        super().__init__(person_id, name, age, gender)
        self.specialization = specialization
        self.patients_assigned = []

class Nurse(Person):
    def __init__(self, person_id, name, age, gender, assigned_ward, shift_time):
        super().__init__(person_id, name, age, gender)
        self.assigned_ward = assigned_ward
        self.shift_time = shift_time

class Patient(Person):
    def __init__(self, person_id, name, age, gender, symptoms, medical_history=None):
        super().__init__(person_id, name, age, gender)
        self.symptoms = symptoms
        self.medical_history = medical_history if medical_history else []
        self.assigned_doctor = None

# Appointment

class Appointment:
    def __init__(self, appointment_id, doctor, patient, date_time):
        self.appointment_id = appointment_id
        self.doctor = doctor
        self.patient = patient
        self.date_time = date_time
        self.status = "Scheduled"

    def add_entry(self):
        print(f"Appointment {self.appointment_id} added: {self.patient.name} with Dr. {self.doctor.name} at {self.date_time}")

    def view_history(self):
        print(f"Appointment ID: {self.appointment_id}, Doctor: {self.doctor.name}, Patient: {self.patient.name}, Date: {self.date_time}, Status: {self.status}")

# Medical Record
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
        print(f"Medical record {self.record_id} added for patient {self.patient.name}")

    def view_history(self):
        print(f"Record ID: {self.record_id}, Patient: {self.patient.name}, Diagnosis: {self.diagnosis}, Prescription: {self.prescription}, Doctor: {self.doctor.name}, Date: {self.date}")

# Hospital System (Manager)
class HospitalSystem:
    def __init__(self):
        self.patients = {}
        self.staff = {}
        self.appointments = {}
        self.records = {}

    def add_person(self, person):
        if isinstance(person, Patient):
            self.patients[person.person_id] = person
        else:
            self.staff[person.person_id] = person
        print(f"{person.name} added successfully.")

    def find_person_by_id(self, person_id):
        return self.patients.get(person_id) or self.staff.get(person_id)

    def create_appointment(self, appointment):
        self.appointments[appointment.appointment_id] = appointment
        appointment.add_entry()

    def assign_doctor_to_patient(self, doctor_id, patient_id):
        doctor = self.find_person_by_id(doctor_id)
        patient = self.find_person_by_id(patient_id)
        if doctor and patient:
            patient.assigned_doctor = doctor
            doctor.patients_assigned.append(patient)
            print(f"Dr. {doctor.name} assigned to patient {patient.name}.")

    def log_medical_record(self, record):
        self.records[record.record_id] = record
        record.add_entry()

    def view_all_appointments(self):
        for appt in self.appointments.values():
            appt.view_history()

hospital = HospitalSystem()

# Add staff
doctor1 = Doctor(1, "Alice Smith", 45, "Female", "Cardiology")
nurse1 = Nurse(2, "Bob Johnson", 30, "Male", "Ward A", "Morning")
hospital.add_person(doctor1)
hospital.add_person(nurse1)

# Add patient
patient1 = Patient(101, "Charlie Brown", 25, "Male", "Fever and cough")
hospital.add_person(patient1)

# Assign doctor to patient
hospital.assign_doctor_to_patient(1, 101)

# Create appointment
appointment1 = Appointment(1001, doctor1, patient1, datetime(2026, 1, 5, 10, 0))
hospital.create_appointment(appointment1)

# Log medical record
record1 = MedicalRecord(5001, patient1, "Flu", "Rest and hydration", doctor1, datetime(2026, 1, 5))
hospital.log_medical_record(record1)

# View appointments
hospital.view_all_appointments()

# View patient's medical history
for record in patient1.medical_history:
    record.view_history()
