from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.data_store import get_waiting_queue, get_patient_by_id, get_available_bed, update_encounter_status, update_bed

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/')
def view_queue():
    waiting_encounters = get_waiting_queue()
    display_data = []
    
    for enc in waiting_encounters:
        patient = get_patient_by_id(enc['patient_id'])
        if patient:
            display_data.append({
                'encounter_id': enc['id'],
                'triage_level': enc['triage_level'],
                'arrival_time': enc['arrival_time'],
                'patient_name': patient['name'],
                'patient_cedula': patient['cedula'],
                'symptoms': enc['symptoms']
            })
            
    return render_template('queue.html', queue=display_data)

@queue_bp.route('/attend/<encounter_id>', methods=['POST'])
def attend_next(encounter_id):
    bed = get_available_bed()
    if not bed:
        flash('No hay camas disponibles actualmente.', 'error')
        return redirect(url_for('queue.view_queue'))
        
    # Asignar cama
    update_bed(bed['id'], 'Occupied', encounter_id)
    # Actualizar encuentro
    update_encounter_status(encounter_id, 'Attended')
    
    flash(f'Paciente asignado a la cama {bed["bed_number"]}.', 'success')
    return redirect(url_for('beds.view_beds'))
