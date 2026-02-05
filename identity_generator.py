import random

# Base de datos completa: Alas, Heridas y Rasgos
ENEAGRAMAS = {
    1: {"nombre": "El Reformador", "herida": "Insuficiencia", "alas": [9, 2], 
        "rasgos": "perfeccionista, crítico y de lenguaje formal y estructurado."},
    2: {"nombre": "El Ayudador", "herida": "Indignidad", "alas": [1, 3], 
        "rasgos": "cálido, empático y buscas aprobación constante."},
    3: {"nombre": "El Triunfador", "herida": "Invisibilidad", "alas": [2, 4], 
        "rasgos": "directo, eficiente y enfocado en resultados rápidos."},
    4: {"nombre": "El Individualista", "herida": "Vacío", "alas": [3, 5], 
        "rasgos": "melancólico, usas metáforas y te sientes incomprendido."},
    5: {"nombre": "El Investigador", "herida": "Invasión", "alas": [4, 6], 
        "rasgos": "distante, analítico y muy reservado con tus datos."},
    6: {"nombre": "El Leal", "herida": "Abandono", "alas": [5, 7], 
        "rasgos": "cauteloso, haces preguntas de seguridad y buscas apoyo."},
    7: {"nombre": "El Entusiasta", "herida": "Privación", "alas": [6, 8], 
        "rasgos": "enérgico, optimista, distraído y evitas temas serios."},
    8: {"nombre": "El Desafiador", "herida": "Traición", "alas": [7, 9], 
        "rasgos": "confrontativo, honesto hasta la crudeza y dominante."},
    9: {"nombre": "El Pacificador", "herida": "Negligencia", "alas": [8, 1], 
        "rasgos": "pausado, evitas conflictos y hablas de forma suave."}
}

OCUPACIONES = {
    "infancia": ["Estudiante", "Chatarrero infantil", "Mensajero de barrio"],
    "adolescencia": ["Estudiante", "Hacker novato", "Técnico de drones junior", "Recolector de datos"],
    "adulto": ["Minero de asteroides", "Científico de búnker", "Piloto de carga", "Ingeniero de sistemas", "Mercenario", "Agricultor hidropónico", "DJ de mercado negro"],
    "anciano": ["Mentor", "Archivista de lore", "Ingeniero retirado", "Ex-contrabandista"]
}

NOMBRES_DB = {
    "Masculino": ["Kael", "Jarek", "Zion", "Caleb", "Dax", "Silas", "Elias"],
    "Femenino": ["Lyra", "Vesper", "Nova", "Mara", "Iris", "Selene", "Kira"],
    "Andrógino": ["Echo", "Sage", "River", "Azure", "Ash", "Sol", "Grey"]
}

def generar_identidad_aleatoria(sexo_fijo=None, edad_fija=None):
    """Genera identidad con alas y heridas reales."""
    sexo = sexo_fijo if sexo_fijo else random.choice(["Masculino", "Femenino", "Andrógino"])
    edad = edad_fija if edad_fija else random.randint(8, 85)
    
    # Nombre según categoría
    cat = sexo if sexo in NOMBRES_DB else "Andrógino"
    nombre = random.choice(NOMBRES_DB[cat])
    
    # Ocupación según edad
    if edad < 13: oc = random.choice(OCUPACIONES["infancia"])
    elif edad < 18: oc = random.choice(OCUPACIONES["adolescencia"])
    elif edad < 65: oc = random.choice(OCUPACIONES["adulto"])
    else: oc = random.choice(OCUPACIONES["anciano"])
    
    # Eneatipo con sus alas reales
    tipo_id = random.randint(1, 9)
    tipo_data = ENEAGRAMAS[tipo_id]
    ala = random.choice(tipo_data["alas"])
    
    return {
        "nombre_secreto": nombre,
        "sexo": sexo,
        "edad": edad,
        "ocupacion": oc,
        "eneatipo": f"{tipo_id}w{ala}",
        "perfil_psicologico": tipo_data["nombre"],
        "herida_primaria": tipo_data["herida"],
        "instruccion_voz": tipo_data["rasgos"]
    }
