def calculate_triage_level(symptoms, heart_rate, respiratory_rate, temperature):
    """
    Algoritmo hipotético muy básico de triaje.
    Retorna un entero del 1 al 5 representando la prioridad (1 = Resucitación, 5 = No Urgente)
    """
    symptoms = symptoms.lower()
    
    # 1. Resucitación (Requiere intervención inmediata para salvar la vida)
    if 'paro' in symptoms or 'inconsciente' in symptoms or 'sin pulso' in symptoms:
        return 1
        
    if heart_rate == 0 or respiratory_rate == 0:
         return 1

    # 2. Emergente (Alto riesgo de deterioro)
    if 'dolor pecho' in symptoms or 'hemorragia' in symptoms or 'dificultad respirar' in symptoms:
        return 2
        
    if temperature > 40.0 or heart_rate > 130:
        return 2

    # 3. Urgente (Estable, requiere múltiples recursos para evaluar)
    if 'fractura' in symptoms or 'dolor abdominal' in symptoms or 'vomito' in symptoms:
        return 3
        
    if temperature > 38.5:
        return 3

    # 4. Menos Urgente (Estable, requiere solo un tipo de recurso)
    if 'dolor cabeza' in symptoms or 'fiebre leve' in symptoms or 'cortada' in symptoms:
        return 4

    # 5. No Urgente (Estable, no requiere recursos)
    return 5

def get_triage_color(level):
    colors = {
        1: 'red',
        2: 'orange',
        3: 'yellow',
        4: 'green',
        5: 'blue'
    }
    return colors.get(level, 'gray')
