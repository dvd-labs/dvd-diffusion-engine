# identity_generator.py
import random

ENEAGRAMAS = {
    1: {"nombre": "El Reformador", "herida": "Crítica / Insuficiencia", "alas": [9, 2]},
    2: {"nombre": "El Ayudador", "herida": "Rechazo / Indignidad", "alas": [1, 3]},
    3: {"nombre": "El Triunfador", "herida": "Invisibilidad / Desprecio", "alas": [2, 4]},
    4: {"nombre": "El Individualista", "herida": "Incomprensión / Vacío", "alas": [3, 5]},
    5: {"nombre": "El Investigador", "herida": "Intrusión / Invasión", "alas": [4, 6]},
    6: {"nombre": "El Leal", "herida": "Abandono / Desprotección", "alas": [5, 7]},
    7: {"nombre": "El Entusiasta", "herida": "Privación / Dolor", "alas": [6, 8]},
    8: {"nombre": "El Desafiador", "herida": "Traición / Vulnerabilidad", "alas": [7, 9]},
    9: {"nombre": "El Pacificador", "herida": "Negligencia / Inexistencia", "alas": [8, 1]}
}

OCUPACIONES = {
    "infancia": ["Estudiante", "Chatarrero infantil", "Aprendiz de mecánica", "Mensajero de barrio"],
    "adolescencia": ["Estudiante", "Hacker novato", "Técnico de drones junior", "Recolector de datos"],
    "adulto": ["Minero de asteroides", "Científico de búnker", "Piloto de carga", "Ingeniero de sistemas", "Mercenario", "Agricultor hidropónico", "DJ de mercado negro"],
    "anciano": ["Mentor", "Archivista de lore", "Ingeniero retirado", "Ermitaño de la estación", "Ex-contrabandista"]
}

def generar_identidad_aleatoria():
    # 1. Parámetros básicos
    sexo = random.choice(["Masculino", "Femenino", "No binario"])
    edad = random.randint(8, 85) # Permite menores de edad
    
    # 2. Selección de ocupación según edad
    if edad < 13: oc = random.choice(OCUPACIONES["infancia"])
    elif edad < 18: oc = random.choice(OCUPACIONES["adolescencia"])
    elif edad < 65: oc = random.choice(OCUPACIONES["adulto"])
    else: oc = random.choice(OCUPACIONES["anciano"])
    
    # 3. Lógica de Eneagrama
    tipo_id = random.randint(1, 9)
    tipo_data = ENEAGRAMAS[tipo_id]
    ala = random.choice(tipo_data["alas"])
    
    return {
        "nombre_clave": "PENDIENTE", # Se definirá en la primera charla
        "sexo": sexo,
        "edad": edad,
        "ocupacion": oc,
        "eneatipo": f"{tipo_id}w{ala}",
        "perfil_psicologico": tipo_data["nombre"],
        "herida_primaria": tipo_data["herida"]
    }
