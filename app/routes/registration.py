from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.data_store import get_patient_by_cedula, add_patient, add_encounter
from app.services.triage import calculate_triage_level

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        
        symptoms = request.form.get('symptoms')
        heart_rate = int(request.form.get('heart_rate', 80))
        resp_rate = int(request.form.get('resp_rate', 16))
        temperature = float(request.form.get('temp', 37.0))

        # Verificar si el paciente existe
        patient = get_patient_by_cedula(cedula)
        if not patient:
            patient_id = add_patient({
                'cedula': cedula,
                'name': name,
                'age': age,
                'gender': gender
            })
        else:
            patient_id = patient['id']

        # Calcular Triaje
        triage_level = calculate_triage_level(symptoms, heart_rate, resp_rate, temperature)
        
        # Añadir Encuentro
        add_encounter({
            'patient_id': patient_id,
            'triage_level': triage_level,
            'symptoms': symptoms,
        })
        
        flash('Paciente registrado y clasificado exitosamente.', 'success')
        return redirect(url_for('queue.view_queue'))

    return render_template('register.html')
