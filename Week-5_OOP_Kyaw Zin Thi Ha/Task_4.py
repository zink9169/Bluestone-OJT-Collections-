from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Optional, Any

def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def _parse_datetime(dt_str: str) -> str:
    """
    Accepts input like:
      - "2026-01-05 14:30"
      - "2026-01-05T14:30"
    Stores ISO string "YYYY-MM-DDTHH:MM:SS"
    """
    dt_str = dt_str.strip()
    if "T" in dt_str:
        fmt_candidates = ["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"]
    else:
        fmt_candidates = ["%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"]

    last_err = None
    for fmt in fmt_candidates:
        try:
            return datetime.strptime(dt_str, fmt).isoformat(timespec="seconds")
        except ValueError as e:
            last_err = e

    raise ValueError("Invalid datetime format. Use 'YYYY-MM-DD HH:MM' (e.g., 2026-01-05 14:30).") from last_err

def _pretty_dt(iso_str: str) -> str:
    try:
        return datetime.fromisoformat(iso_str).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso_str

def read_int(prompt: str) -> int:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        raise ValueError("Please enter a valid integer.")

def read_nonempty(prompt: str) -> str:
    s = input(prompt).strip()
    if not s:
        raise ValueError("Input cannot be empty.")
    return s

def read_choice(prompt: str, allowed: List[str]) -> str:
    c = input(prompt).strip()
    if c not in allowed:
        raise ValueError(f"Invalid choice. Allowed: {', '.join(allowed)}")
    return c




@dataclass
class Person:
    name: str
    age: int
    gender: str
    person_id: int

    @property
    def role(self) -> str:
        return "Person"


@dataclass
class Doctor(Person):
    specialization: str
    schedule: List[str] = field(default_factory=list)           # list of ISO datetime strings or notes
    patients_assigned: List[int] = field(default_factory=list)  # patient_ids

    @property
    def role(self) -> str:
        return "Doctor"


@dataclass
class Nurse(Person):
    assigned_ward: str
    shift_time: str

    @property
    def role(self) -> str:
        return "Nurse"


@dataclass
class Patient(Person):
    symptoms: str = ""
    medical_history: List[str] = field(default_factory=list)     # simple text history
    assigned_doctor: Optional[int] = None                        # doctor_id

    @property
    def role(self) -> str:
        return "Patient"




@dataclass
class Appointment:
    appointment_id: int
    doctor_id: int
    patient_id: int
    datetime_iso: str
    status: str = "BOOKED"  
    history: List[Dict[str, str]] = field(default_factory=list)

    def add_entry(self, note: str) -> None:
        self.history.append({"timestamp": _now_iso(), "note": note})

    def view_history(self) -> None:
        if not self.history:
            print("No appointment history entries.")
            return
        print("-" * 60)
        print(f"Appointment History (ID: {self.appointment_id})")
        for h in self.history:
            print(f"{_pretty_dt(h['timestamp'])}: {h['note']}")
        print("-" * 60)


@dataclass
class MedicalRecord:
    record_id: int
    patient_id: int
    diagnosis: str
    prescription: str
    doctor_id: int
    date_iso: str
    history: List[Dict[str, str]] = field(default_factory=list)

    def add_entry(self, note: str) -> None:
        self.history.append({"timestamp": _now_iso(), "note": note})

    def view_history(self) -> None:
        if not self.history:
            print("No record history entries.")
            return
        print("-" * 60)
        print(f"MedicalRecord History (Record ID: {self.record_id})")
        for h in self.history:
            print(f"{_pretty_dt(h['timestamp'])}: {h['note']}")
        print("-" * 60)




class HospitalSystem:
    def __init__(self) -> None:
        self.patients: Dict[int, Patient] = {}
        self.staff: Dict[int, Person] = {}  
        self.appointments: Dict[int, Appointment] = {}
        self.records: Dict[int, MedicalRecord] = {}

        self._next_person_id = 1001
        self._next_appointment_id = 5001
        self._next_record_id = 8001

    # ---- Core methods ----

    def add_person(self, person: Person) -> None:
        if isinstance(person, Patient):
            self.patients[person.person_id] = person
        else:
            self.staff[person.person_id] = person

    def find_person_by_id(self, person_id: int) -> Optional[Person]:
        if person_id in self.patients:
            return self.patients[person_id]
        if person_id in self.staff:
            return self.staff[person_id]
        return None

    def create_appointment(self, doctor_id: int, patient_id: int, datetime_iso: str) -> Appointment:
        doctor = self.staff.get(doctor_id)
        patient = self.patients.get(patient_id)

        if not isinstance(doctor, Doctor):
            raise ValueError("Doctor not found or invalid doctor ID.")
        if not isinstance(patient, Patient):
            raise ValueError("Patient not found or invalid patient ID.")

        appt_id = self._next_appointment_id
        self._next_appointment_id += 1

        appt = Appointment(
            appointment_id=appt_id,
            doctor_id=doctor_id,
            patient_id=patient_id,
            datetime_iso=datetime_iso,
            status="BOOKED",
        )
        appt.add_entry("Appointment created (BOOKED).")
        self.appointments[appt_id] = appt
        return appt

    def cancel_appointment(self, appointment_id: int, reason: str = "Cancelled by receptionist.") -> None:
        appt = self.appointments.get(appointment_id)
        if not appt:
            raise ValueError("Appointment not found.")
        appt.status = "CANCELLED"
        appt.add_entry(f"Status changed to CANCELLED. Reason: {reason}")

    def assign_doctor_to_patient(self, doctor_id: int, patient_id: int) -> None:
        doctor = self.staff.get(doctor_id)
        patient = self.patients.get(patient_id)

        if not isinstance(doctor, Doctor):
            raise ValueError("Doctor not found.")
        if not isinstance(patient, Patient):
            raise ValueError("Patient not found.")

        patient.assigned_doctor = doctor_id
        if patient_id not in doctor.patients_assigned:
            doctor.patients_assigned.append(patient_id)

    def log_medical_record(self, doctor_id: int, patient_id: int, diagnosis: str, prescription: str) -> MedicalRecord:
        doctor = self.staff.get(doctor_id)
        patient = self.patients.get(patient_id)

        if not isinstance(doctor, Doctor):
            raise ValueError("Doctor not found.")
        if not isinstance(patient, Patient):
            raise ValueError("Patient not found.")

        rec_id = self._next_record_id
        self._next_record_id += 1

        record = MedicalRecord(
            record_id=rec_id,
            patient_id=patient_id,
            diagnosis=diagnosis.strip(),
            prescription=prescription.strip(),
            doctor_id=doctor_id,
            date_iso=_now_iso(),
        )
        record.add_entry("Medical record created.")
        self.records[rec_id] = record

    
        patient.medical_history.append(f"{_pretty_dt(record.date_iso)}: Dx={record.diagnosis}, Rx={record.prescription} (Dr {doctor_id})")
        return record

    def view_all_appointments(self) -> None:
        if not self.appointments:
            print("No appointments found.")
            return
        print("\nAll Appointments")
        print("-" * 80)
        for appt in sorted(self.appointments.values(), key=lambda a: a.datetime_iso):
            d = self.staff.get(appt.doctor_id)
            p = self.patients.get(appt.patient_id)
            dname = d.name if isinstance(d, Doctor) else f"Doctor#{appt.doctor_id}"
            pname = p.name if isinstance(p, Patient) else f"Patient#{appt.patient_id}"
            print(f"ID {appt.appointment_id} | {_pretty_dt(appt.datetime_iso)} | Dr: {dname} | Pt: {pname} | {appt.status}")
        print("-" * 80)

    def list_doctors(self) -> None:
        doctors = [s for s in self.staff.values() if isinstance(s, Doctor)]
        if not doctors:
            print("No doctors registered.")
            return
        print("\nDoctors")
        print("-" * 60)
        for d in doctors:
            print(f"ID {d.person_id} | {d.name} | {d.specialization}")
        print("-" * 60)

    def list_patients(self) -> None:
        if not self.patients:
            print("No patients registered.")
            return
        print("\nPatients")
        print("-" * 60)
        for p in self.patients.values():
            ad = p.assigned_doctor if p.assigned_doctor else "None"
            print(f"ID {p.person_id} | {p.name} | Age {p.age} | Assigned Doctor: {ad}")
        print("-" * 60)

    

    def new_person_id(self) -> int:
        pid = self._next_person_id
        self._next_person_id += 1
        return pid

    

    def save_data(self, path: str = "hospital_data.json") -> None:
        data = {
            "meta": {
                "next_person_id": self._next_person_id,
                "next_appointment_id": self._next_appointment_id,
                "next_record_id": self._next_record_id,
            },
            "patients": [self._person_to_dict(p) for p in self.patients.values()],
            "staff": [self._person_to_dict(s) for s in self.staff.values()],
            "appointments": [asdict(a) for a in self.appointments.values()],
            "records": [asdict(r) for r in self.records.values()],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {path}")

    def load_data(self, path: str = "hospital_data.json") -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("No saved data file found. Starting new system.")
            return

        self.patients.clear()
        self.staff.clear()
        self.appointments.clear()
        self.records.clear()

        meta = data.get("meta", {})
        self._next_person_id = int(meta.get("next_person_id", 1001))
        self._next_appointment_id = int(meta.get("next_appointment_id", 5001))
        self._next_record_id = int(meta.get("next_record_id", 8001))

        for p in data.get("patients", []):
            person = self._dict_to_person(p)
            if isinstance(person, Patient):
                self.patients[person.person_id] = person

        for s in data.get("staff", []):
            person = self._dict_to_person(s)
            if isinstance(person, (Doctor, Nurse, Person)) and not isinstance(person, Patient):
                self.staff[person.person_id] = person

        for a in data.get("appointments", []):
            appt = Appointment(**a)
            self.appointments[appt.appointment_id] = appt

        for r in data.get("records", []):
            rec = MedicalRecord(**r)
            self.records[rec.record_id] = rec

        print(f"Data loaded from {path}")

    

    @staticmethod
    def _person_to_dict(person: Person) -> Dict[str, Any]:
        d = asdict(person)
        d["_class"] = person.__class__.__name__
        return d

    @staticmethod
    def _dict_to_person(d: Dict[str, Any]) -> Person:
        cls = d.get("_class", "Person")
        d = dict(d)
        d.pop("_class", None)

        if cls == "Doctor":
            return Doctor(**d)
        if cls == "Nurse":
            return Nurse(**d)
        if cls == "Patient":
            return Patient(**d)
        return Person(**d)




class HospitalApp:
    def __init__(self) -> None:
        self.system = HospitalSystem()

    def seed_if_empty(self) -> None:
        """Optional: create one doctor and one nurse so you can test quickly."""
        if not self.system.staff:
            d1 = Doctor(
                name="Dr. Aung",
                age=45,
                gender="M",
                person_id=self.system.new_person_id(),
                specialization="General Medicine",
                schedule=[],
                patients_assigned=[],
            )
            n1 = Nurse(
                name="Nurse Hnin",
                age=30,
                gender="F",
                person_id=self.system.new_person_id(),
                assigned_ward="Ward A",
                shift_time="Day",
            )
            self.system.add_person(d1)
            self.system.add_person(n1)

    def run(self) -> None:
        self.system.load_data()
        self.seed_if_empty()

        while True:
            print("\nPlease log in as:")
            print("1. Doctor")
            print("2. Nurse")
            print("3. Receptionist")
            print("4. Patient")
            print("5. Exit")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3", "4", "5"])
                if choice == "1":
                    self.doctor_login()
                elif choice == "2":
                    self.nurse_login()
                elif choice == "3":
                    self.receptionist_menu()
                elif choice == "4":
                    self.patient_login()
                elif choice == "5":
                    self.system.save_data()
                    print("Goodbye.")
                    return
            except ValueError as e:
                print(f"Error: {e}")



    def doctor_login(self) -> None:
        self.system.list_doctors()
        try:
            doc_id = read_int("Enter Doctor ID: ")
            doc = self.system.staff.get(doc_id)
            if not isinstance(doc, Doctor):
                raise ValueError("Invalid Doctor ID.")
            self.doctor_menu(doc)
        except ValueError as e:
            print(f"Error: {e}")

    def nurse_login(self) -> None:
    
        nurses = [s for s in self.system.staff.values() if isinstance(s, Nurse)]
        if not nurses:
            print("No nurses registered.")
            return
        print("\nNurses")
        print("-" * 60)
        for n in nurses:
            print(f"ID {n.person_id} | {n.name} | Ward {n.assigned_ward} | Shift {n.shift_time}")
        print("-" * 60)

        try:
            nurse_id = read_int("Enter Nurse ID: ")
            nurse = self.system.staff.get(nurse_id)
            if not isinstance(nurse, Nurse):
                raise ValueError("Invalid Nurse ID.")
            self.nurse_menu(nurse)
        except ValueError as e:
            print(f"Error: {e}")

    def patient_login(self) -> None:
        self.system.list_patients()
        try:
            pid = read_int("Enter Patient ID: ")
            p = self.system.patients.get(pid)
            if not isinstance(p, Patient):
                raise ValueError("Invalid Patient ID.")
            self.patient_menu(p)
        except ValueError as e:
            print(f"Error: {e}")


    def doctor_menu(self, doctor: Doctor) -> None:
        while True:
            print(f"\nDoctor Menu (Dr. {doctor.name} | ID {doctor.person_id})")
            print("1. View Appointments")
            print("2. Log Medical Record")
            print("3. View Patient History")
            print("4. Logout")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3", "4"])
                if choice == "1":
                    self.view_doctor_appointments(doctor.person_id)
                elif choice == "2":
                    self.doctor_log_record(doctor.person_id)
                elif choice == "3":
                    self.doctor_view_patient_history(doctor.person_id)
                elif choice == "4":
                    return
            except ValueError as e:
                print(f"Error: {e}")

    def view_doctor_appointments(self, doctor_id: int) -> None:
        appts = [a for a in self.system.appointments.values() if a.doctor_id == doctor_id]
        if not appts:
            print("No appointments for this doctor.")
            return

        print("\nDoctor Appointments")
        print("-" * 80)
        for a in sorted(appts, key=lambda x: x.datetime_iso):
            p = self.system.patients.get(a.patient_id)
            pname = p.name if p else f"Patient#{a.patient_id}"
            print(f"ID {a.appointment_id} | {_pretty_dt(a.datetime_iso)} | Patient: {pname} | {a.status}")
        print("-" * 80)


        view_hist = input("View an appointment history? (y/n): ").strip().lower()
        if view_hist == "y":
            appt_id = read_int("Appointment ID: ")
            appt = self.system.appointments.get(appt_id)
            if appt and appt.doctor_id == doctor_id:
                appt.view_history()
            else:
                print("Appointment not found or not assigned to this doctor.")

    def doctor_log_record(self, doctor_id: int) -> None:
        self.system.list_patients()
        patient_id = read_int("Patient ID: ")
        diagnosis = read_nonempty("Diagnosis: ")
        prescription = read_nonempty("Prescription: ")
        record = self.system.log_medical_record(doctor_id, patient_id, diagnosis, prescription)
        print(f"Medical record logged successfully. Record ID: {record.record_id}")

    def doctor_view_patient_history(self, doctor_id: int) -> None:
        self.system.list_patients()
        patient_id = read_int("Patient ID: ")
        patient = self.system.patients.get(patient_id)
        if not patient:
            print("Patient not found.")
            return

        print("\nPatient Basic Info")
        print("-" * 60)
        print(f"ID: {patient.person_id} | Name: {patient.name} | Age: {patient.age} | Gender: {patient.gender}")
        print(f"Assigned Doctor ID: {patient.assigned_doctor}")
        print(f"Symptoms: {patient.symptoms}")
        print("-" * 60)

        print("\nMedical History (simple text entries)")
        if not patient.medical_history:
            print("No medical history entries.")
        else:
            for line in patient.medical_history:
                print(f"- {line}")

      
        print("\nMedical Records (structured)")
        patient_records = [r for r in self.system.records.values() if r.patient_id == patient_id]
        if not patient_records:
            print("No medical records found.")
        else:
            for r in sorted(patient_records, key=lambda x: x.date_iso, reverse=True):
                print("-" * 70)
                print(f"Record ID: {r.record_id} | Date: {_pretty_dt(r.date_iso)} | Doctor ID: {r.doctor_id}")
                print(f"Diagnosis: {r.diagnosis}")
                print(f"Prescription: {r.prescription}")
            print("-" * 70)

            view_hist = input("View a medical record history? (y/n): ").strip().lower()
            if view_hist == "y":
                rid = read_int("Record ID: ")
                rec = self.system.records.get(rid)
                if rec and rec.patient_id == patient_id:
                    rec.view_history()
                else:
                    print("Record not found for that patient.")

 

    def receptionist_menu(self) -> None:
        while True:
            print("\nReceptionist Menu")
            print("1. Register Patient")
            print("2. Book Appointment")
            print("3. Assign Doctor")
            print("4. Cancel Appointment")
            print("5. View All Appointments")
            print("6. Logout")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3", "4", "5", "6"])
                if choice == "1":
                    self.register_patient()
                elif choice == "2":
                    self.book_appointment()
                elif choice == "3":
                    self.assign_doctor()
                elif choice == "4":
                    self.cancel_appointment()
                elif choice == "5":
                    self.system.view_all_appointments()
                elif choice == "6":
                    return
            except ValueError as e:
                print(f"Error: {e}")

    def register_patient(self) -> None:
        name = read_nonempty("Patient name: ")
        age = read_int("Age: ")
        gender = read_nonempty("Gender: ")
        symptoms = input("Symptoms (optional): ").strip()

        patient = Patient(
            name=name,
            age=age,
            gender=gender,
            person_id=self.system.new_person_id(),
            symptoms=symptoms,
            medical_history=[],
            assigned_doctor=None,
        )
        self.system.add_person(patient)
        print(f"Patient registered successfully. Patient ID: {patient.person_id}")

    def book_appointment(self) -> None:
        self.system.list_patients()
        patient_id = read_int("Patient ID: ")

        self.system.list_doctors()
        doctor_id = read_int("Doctor ID: ")

        dt_in = read_nonempty("Appointment datetime (YYYY-MM-DD HH:MM): ")
        dt_iso = _parse_datetime(dt_in)

        appt = self.system.create_appointment(doctor_id, patient_id, dt_iso)
        print(f"Appointment booked successfully. Appointment ID: {appt.appointment_id}")

    def assign_doctor(self) -> None:
        self.system.list_patients()
        patient_id = read_int("Patient ID: ")

        self.system.list_doctors()
        doctor_id = read_int("Doctor ID: ")

        self.system.assign_doctor_to_patient(doctor_id, patient_id)
        print("Doctor assigned successfully.")

    def cancel_appointment(self) -> None:
        self.system.view_all_appointments()
        appt_id = read_int("Appointment ID to cancel: ")
        reason = input("Reason (optional): ").strip() or "Cancelled by receptionist."
        self.system.cancel_appointment(appt_id, reason)
        print("Appointment cancelled successfully.")


    def nurse_menu(self, nurse: Nurse) -> None:
        while True:
            print(f"\nNurse Menu ({nurse.name} | Ward {nurse.assigned_ward} | Shift {nurse.shift_time})")
            print("1. View All Appointments")
            print("2. View Patients")
            print("3. Logout")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3"])
                if choice == "1":
                    self.system.view_all_appointments()
                elif choice == "2":
                    self.system.list_patients()
                elif choice == "3":
                    return
            except ValueError as e:
                print(f"Error: {e}")


    def patient_menu(self, patient: Patient) -> None:
        while True:
            print(f"\nPatient Menu ({patient.name} | ID {patient.person_id})")
            print("1. View My Appointments")
            print("2. View My Medical History")
            print("3. Logout")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3"])
                if choice == "1":
                    self.view_patient_appointments(patient.person_id)
                elif choice == "2":
                    self.view_patient_history(patient.person_id)
                elif choice == "3":
                    return
            except ValueError as e:
                print(f"Error: {e}")

    def view_patient_appointments(self, patient_id: int) -> None:
        appts = [a for a in self.system.appointments.values() if a.patient_id == patient_id]
        if not appts:
            print("No appointments found.")
            return

        print("\nMy Appointments")
        print("-" * 80)
        for a in sorted(appts, key=lambda x: x.datetime_iso):
            d = self.system.staff.get(a.doctor_id)
            dname = d.name if isinstance(d, Doctor) else f"Doctor#{a.doctor_id}"
            print(f"ID {a.appointment_id} | {_pretty_dt(a.datetime_iso)} | Doctor: {dname} | {a.status}")
        print("-" * 80)

    def view_patient_history(self, patient_id: int) -> None:
        p = self.system.patients.get(patient_id)
        if not p:
            print("Patient not found.")
            return

        print("\nMy Medical History (simple text entries)")
        if not p.medical_history:
            print("No medical history entries.")
        else:
            for line in p.medical_history:
                print(f"- {line}")

        print("\nMy Medical Records (structured)")
        recs = [r for r in self.system.records.values() if r.patient_id == patient_id]
        if not recs:
            print("No medical records found.")
            return

        for r in sorted(recs, key=lambda x: x.date_iso, reverse=True):
            print("-" * 70)
            print(f"Record ID: {r.record_id} | Date: {_pretty_dt(r.date_iso)} | Doctor ID: {r.doctor_id}")
            print(f"Diagnosis: {r.diagnosis}")
            print(f"Prescription: {r.prescription}")
        print("-" * 70)


if __name__ == "__main__":
    HospitalApp().run()
