# app/codein.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date, datetime
import uuid

# Initialize the APIRouter for this file's routes
# All routes defined here will have a common prefix (if specified) and tags
router = APIRouter(
    prefix="/d", # Optional: Adds a /demo prefix to all routes in this file
    tags=["In-Memory Demo Data"], # Groups these routes in Swagger UI
)

# --- 1. Define Pydantic Schemas ---
# These define the structure of your data for request bodies and response models.

class PatientBase(BaseModel):
    name: str
    date_of_birth: date
    approx_age: Optional[int] = None # Optional, can be derived from DOB
    # Add other fields you might eventually want, e.g., gender, address, phone

class PatientCreate(PatientBase):
    pass # For creation, often same as base, but could have required fields not in base

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    approx_age: Optional[int] = None

class Patient(PatientBase):
    id: uuid.UUID
    # Add timestamps if needed, but keeping it minimal for demo
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True # Enables Pydantic to read data from ORM models (not used directly here, but good practice)


class MedicineBase(BaseModel):
    name: str
    quantity: int = Field(..., ge=0) # Quantity must be >= 0

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)

class Medicine(MedicineBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    patient_id: uuid.UUID
    appointment_time: datetime
    diagnosis: Optional[str] = None
    # Add other fields like doctor_id, clinic, status etc.

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    patient_id: Optional[uuid.UUID] = None
    appointment_time: Optional[datetime] = None
    diagnosis: Optional[str] = None

class Appointment(AppointmentBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class PrescriptionBase(BaseModel):
    appointment_id: uuid.UUID
    patient_id: uuid.UUID
    medicine_id: uuid.UUID
    quantity: int = Field(..., ge=1)
    prescribed_at: datetime

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(BaseModel):
    appointment_id: Optional[uuid.UUID] = None
    patient_id: Optional[uuid.UUID] = None
    medicine_id: Optional[uuid.UUID] = None
    quantity: Optional[int] = Field(None, ge=1)
    prescribed_at: Optional[datetime] = None

class Prescription(PrescriptionBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


# --- 2. In-Memory "Databases" (Dictionaries) ---
# These will store our data. Keys are UUIDs, values are Pydantic model instances.
in_memory_patients: Dict[uuid.UUID, Patient] = {}
in_memory_appointments: Dict[uuid.UUID, Appointment] = {}
in_memory_medicines: Dict[uuid.UUID, Medicine] = {}
in_memory_prescriptions: Dict[uuid.UUID, Prescription] = {}


# --- 3. Hardcoded Sample Data (for quick demo) ---

# Patients
patient_id_1 = uuid.uuid4()
patient_id_2 = uuid.uuid4()
in_memory_patients[patient_id_1] = Patient(
    id=patient_id_1,
    name="Alice Smith",
    date_of_birth=date(1985, 1, 15),
    approx_age=39
)
in_memory_patients[patient_id_2] = Patient(
    id=patient_id_2,
    name="Bob Johnson",
    date_of_birth=date(1992, 7, 22),
    approx_age=32
)

# Medicines
medicine_id_1 = uuid.uuid4()
medicine_id_2 = uuid.uuid4()
in_memory_medicines[medicine_id_1] = Medicine(
    id=medicine_id_1,
    name="Aspirin 81mg",
    quantity=100
)
in_memory_medicines[medicine_id_2] = Medicine(
    id=medicine_id_2,
    name="Amoxicillin 500mg",
    quantity=50
)

# Appointments
appointment_id_1 = uuid.uuid4()
appointment_id_2 = uuid.uuid4()
in_memory_appointments[appointment_id_1] = Appointment(
    id=appointment_id_1,
    patient_id=patient_id_1,
    appointment_time=datetime(2025, 8, 20, 10, 0, 0),
    diagnosis="Flu symptoms"
)
in_memory_appointments[appointment_id_2] = Appointment(
    id=appointment_id_2,
    patient_id=patient_id_2,
    appointment_time=datetime(2025, 8, 20, 14, 30, 0),
    diagnosis="Routine check-up"
)

# Prescriptions
prescription_id_1 = uuid.uuid4()
in_memory_prescriptions[prescription_id_1] = Prescription(
    id=prescription_id_1,
    appointment_id=appointment_id_1,
    patient_id=patient_id_1,
    medicine_id=medicine_id_2, # Amoxicillin
    quantity=20,
    prescribed_at=datetime.utcnow()
)


# --- 5. Implement API Endpoints (Routes) using the router ---

# --- Patient Endpoints ---
@router.post("/patients/", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate):
    new_patient_id = uuid.uuid4()
    new_patient = Patient(id=new_patient_id, **patient.dict())
    in_memory_patients[new_patient_id] = new_patient
    return new_patient

@router.get("/patients/", response_model=List[Patient])
async def read_patients():
    return list(in_memory_patients.values())

@router.get("/patients/{patient_id}", response_model=Patient)
async def read_patient(patient_id: uuid.UUID):
    patient = in_memory_patients.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/patients/{patient_id}", response_model=Patient)
async def update_patient(patient_id: uuid.UUID, patient_update: PatientUpdate):
    existing_patient = in_memory_patients.get(patient_id)
    if not existing_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Update only the fields that are provided in the request
    update_data = patient_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_patient, key, value)
    
    in_memory_patients[patient_id] = existing_patient # Re-assign to ensure dict update
    return existing_patient


# --- Medicine Endpoints ---
@router.post("/medicines/", response_model=Medicine, status_code=status.HTTP_201_CREATED)
async def create_medicine(medicine: MedicineCreate):
    new_medicine_id = uuid.uuid4()
    new_medicine = Medicine(id=new_medicine_id, **medicine.dict())
    in_memory_medicines[new_medicine_id] = new_medicine
    return new_medicine

@router.get("/medicines/", response_model=List[Medicine])
async def read_medicines():
    return list(in_memory_medicines.values())

@router.get("/medicines/{medicine_id}", response_model=Medicine)
async def read_medicine(medicine_id: uuid.UUID):
    medicine = in_memory_medicines.get(medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.put("/medicines/{medicine_id}", response_model=Medicine)
async def update_medicine(medicine_id: uuid.UUID, medicine_update: MedicineUpdate):
    existing_medicine = in_memory_medicines.get(medicine_id)
    if not existing_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    update_data = medicine_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_medicine, key, value)
    
    in_memory_medicines[medicine_id] = existing_medicine
    return existing_medicine


# --- Appointment Endpoints ---
@router.post("/appointments/", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: AppointmentCreate):
    # Basic check for patient existence (in this in-memory context)
    if appointment.patient_id not in in_memory_patients:
        raise HTTPException(status_code=400, detail="Patient ID not found for appointment")

    new_appointment_id = uuid.uuid4()
    new_appointment = Appointment(id=new_appointment_id, **appointment.dict())
    in_memory_appointments[new_appointment_id] = new_appointment
    return new_appointment

@router.get("/appointments/", response_model=List[Appointment])
async def read_appointments():
    return list(in_memory_appointments.values())

@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def read_appointment(appointment_id: uuid.UUID):
    appointment = in_memory_appointments.get(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.put("/appointments/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: uuid.UUID, appointment_update: AppointmentUpdate):
    existing_appointment = in_memory_appointments.get(appointment_id)
    if not existing_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if appointment_update.patient_id and appointment_update.patient_id not in in_memory_patients:
        raise HTTPException(status_code=400, detail="Updated Patient ID not found for appointment")

    update_data = appointment_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_appointment, key, value)
    
    in_memory_appointments[appointment_id] = existing_appointment
    return existing_appointment


# --- Prescription Endpoints (Added for completeness based on your schema) ---
@router.post("/prescriptions/", response_model=Prescription, status_code=status.HTTP_201_CREATED)
async def create_prescription(prescription: PrescriptionCreate):
    # Basic checks for foreign key existence
    if prescription.patient_id not in in_memory_patients:
        raise HTTPException(status_code=400, detail="Patient ID not found for prescription")
    if prescription.appointment_id not in in_memory_appointments:
        raise HTTPException(status_code=400, detail="Appointment ID not found for prescription")
    if prescription.medicine_id not in in_memory_medicines:
        raise HTTPException(status_code=400, detail="Medicine ID not found for prescription")

    new_prescription_id = uuid.uuid4()
    new_prescription = Prescription(id=new_prescription_id, **prescription.dict())
    in_memory_prescriptions[new_prescription_id] = new_prescription
    return new_prescription

@router.get("/prescriptions/", response_model=List[Prescription])
async def read_prescriptions():
    return list(in_memory_prescriptions.values())

@router.get("/prescriptions/{prescription_id}", response_model=Prescription)
async def read_prescription(prescription_id: uuid.UUID):
    prescription = in_memory_prescriptions.get(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@router.put("/prescriptions/{prescription_id}", response_model=Prescription)
async def update_prescription(prescription_id: uuid.UUID, prescription_update: PrescriptionUpdate):
    existing_prescription = in_memory_prescriptions.get(prescription_id)
    if not existing_prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    # Basic checks for foreign key existence during update
    if prescription_update.patient_id and prescription_update.patient_id not in in_memory_patients:
        raise HTTPException(status_code=400, detail="Updated Patient ID not found for prescription")
    if prescription_update.appointment_id and prescription_update.appointment_id not in in_memory_appointments:
        raise HTTPException(status_code=400, detail="Updated Appointment ID not found for prescription")
    if prescription_update.medicine_id and prescription_update.medicine_id not in in_memory_medicines:
        raise HTTPException(status_code=400, detail="Updated Medicine ID not found for prescription")

    update_data = prescription_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_prescription, key, value)
    
    in_memory_prescriptions[prescription_id] = existing_prescription
    return existing_prescription
