import json
import os
import uuid
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
PATIENTS_FILE = os.path.join(DATA_DIR, 'patients.json')
ENCOUNTERS_FILE = os.path.join(DATA_DIR, 'encounters.json')
BEDS_FILE = os.path.join(DATA_DIR, 'beds.json')

def _ensure_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def _read_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def _write_json(filepath, data):
    _ensure_dir()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def init_data_store():
    _ensure_dir()
    # Inicializar camas si no existen
    if not os.path.exists(BEDS_FILE):
        beds = []
        for i in range(1, 11): # 10 camas
            beds.append({
                "id": str(uuid.uuid4()),
                "bed_number": f"B{i:02d}",
                "zone": "General",
                "status": "Available",
                "current_encounter_id": None
            })
        _write_json(BEDS_FILE, beds)
    
    if not os.path.exists(PATIENTS_FILE):
        _write_json(PATIENTS_FILE, [])
        
    if not os.path.exists(ENCOUNTERS_FILE):
        _write_json(ENCOUNTERS_FILE, [])

# Operaciones de Pacientes
def get_patients():
    return _read_json(PATIENTS_FILE)

def add_patient(patient_data):
    patients = get_patients()
    patient_id = str(uuid.uuid4())
    patient_data['id'] = patient_id
    patient_data['created_at'] = datetime.now().isoformat()
    patients.append(patient_data)
    _write_json(PATIENTS_FILE, patients)
    return patient_id

def get_patient_by_cedula(cedula):
    patients = get_patients()
    for p in patients:
        if p['cedula'] == cedula:
            return p
    return None

def get_patient_by_id(id):
    patients = get_patients()
    for p in patients:
        if p['id'] == id:
            return p
    return None

# Operaciones de Encuentros
def get_encounters():
    return _read_json(ENCOUNTERS_FILE)

def add_encounter(encounter_data):
    encounters = get_encounters()
    encounter_id = str(uuid.uuid4())
    encounter_data['id'] = encounter_id
    encounter_data['status'] = 'Waiting'
    encounter_data['arrival_time'] = datetime.now().isoformat()
    encounter_data['discharge_time'] = None
    encounters.append(encounter_data)
    _write_json(ENCOUNTERS_FILE, encounters)
    return encounter_id

def update_encounter_status(encounter_id, new_status):
    encounters = get_encounters()
    for idx, e in enumerate(encounters):
        if e['id'] == encounter_id:
            encounters[idx]['status'] = new_status
            if new_status == 'Discharged':
                encounters[idx]['discharge_time'] = datetime.now().isoformat()
            _write_json(ENCOUNTERS_FILE, encounters)
            return True
    return False

def get_waiting_queue():
    encounters = get_encounters()
    # Solo en espera
    waiting = [e for e in encounters if e['status'] == 'Waiting']
    # Ordenar por prioridad (1 es la más alta, por lo que va primero el número menor), luego por hora de llegada
    waiting.sort(key=lambda x: (x['triage_level'], x['arrival_time']))
    return waiting

def get_encounters_by_patient(patient_id):
    encounters = get_encounters()
    return [e for e in encounters if e['patient_id'] == patient_id]

# Operaciones de Camas
def get_beds():
    return _read_json(BEDS_FILE)

def update_bed(bed_id, status, encounter_id=None):
    beds = get_beds()
    for idx, b in enumerate(beds):
        if b['id'] == bed_id:
            beds[idx]['status'] = status
            beds[idx]['current_encounter_id'] = encounter_id
            _write_json(BEDS_FILE, beds)
            return True
    return False

def get_available_bed():
    beds = get_beds()
    for b in beds:
        if b['status'] == 'Available':
            return b
    return None
