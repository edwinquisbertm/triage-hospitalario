from flask import Blueprint, render_template, request, flash
from app.models.data_store import get_patient_by_cedula, get_encounters_by_patient

history_bp = Blueprint('history', __name__)

@history_bp.route('/', methods=['GET'])
def search_history():
    cedula = request.args.get('cedula')
    patient = None
    encounters = []
    
    if cedula:
        patient = get_patient_by_cedula(cedula)
        if patient:
            encounters = get_encounters_by_patient(patient['id'])
            # Ordenar los más recientes primero
            encounters.sort(key=lambda x: x['arrival_time'], reverse=True)
        else:
            flash('No se encontró historial clínico para esa cédula.', 'error')
            
    return render_template('history.html', patient=patient, encounters=encounters, cedula=cedula)
