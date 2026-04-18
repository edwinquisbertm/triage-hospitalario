from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.data_store import get_beds, update_bed, update_encounter_status, get_patient_by_id, get_encounters

beds_bp = Blueprint('beds', __name__)

@beds_bp.route('/')
def view_beds():
    beds = get_beds()
    all_encounters = get_encounters()
    display_beds = []
    
    for b in beds:
        bed_info = dict(b)
        bed_info['patient_name'] = None
        bed_info['triage_level'] = None
        
        if b['current_encounter_id']:
            # Encontrar el encuentro
            enc = next((e for e in all_encounters if e['id'] == b['current_encounter_id']), None)
            if enc:
                patient = get_patient_by_id(enc['patient_id'])
                if patient:
                    bed_info['patient_name'] = patient['name']
                    bed_info['triage_level'] = enc['triage_level']
                    
        display_beds.append(bed_info)
        
    return render_template('beds.html', beds=display_beds)

@beds_bp.route('/discharge/<bed_id>/<encounter_id>', methods=['POST'])
def discharge(bed_id, encounter_id):
    update_encounter_status(encounter_id, 'Discharged')
    update_bed(bed_id, 'Available', None)
    flash('Paciente dado de alta y cama liberada.', 'success')
    return redirect(url_for('beds.view_beds'))
