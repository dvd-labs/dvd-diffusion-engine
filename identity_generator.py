# identity_generator.py
import random

# Base de datos de nombres para variedad total
NOMBRES_DB = {
    "Masculino": ["Kael", "Jarek", "Zion", "Caleb", "Dax", "Silas", "Elias", "Milo", "Vane", "Nico"],
    "Femenino": ["Lyra", "Vesper", "Nova", "Mara", "Iris", "Selene", "Kira", "Hana", "Zaya", "Rhea"],
    "No binario": ["Echo", "Sage", "River", "Azure", "Ash", "Sol", "Grey", "Flint", "Indi", "Lux"]
}

ENEAGRAMAS = {
    1: {"nombre": "El Reformador", "herida": "Insuficiencia", "alas": [9, 2], 
        "rasgos": "Eres perfeccionista, crítico y usas un lenguaje muy estructurado y formal."},
    2: {"nombre": "El Ayudador", "herida": "Indignidad", "alas": [1, 3], 
        "rasgos": "Eres cálido, empático y tiendes a halagar o buscar la aprobación del otro."},
    3: {"nombre": "El Triunfador", "herida": "Invisibilidad", "alas": [2, 4], 
        "rasgos": "Eres directo, eficiente, hablas de logros y detestas perder el tiempo."},
    4: {"nombre": "El Individualista", "herida": "Vacío", "alas": [3, 5], 
        "rasgos": "Eres melancólico, usas metáforas y te enfocas en lo que falta o en lo que es único."},
    5: {"nombre": "El Investigador", "herida": "Invasión", "alas": [4, 6], 
        "rasgos": "Eres distante, analítico, usas pocos datos personales y muchas explicaciones técnicas."},
    6: {"nombre": "El Leal", "herida": "Abandono", "alas": [5, 7], 
        "rasgos": "Eres cauteloso, haces muchas preguntas de seguridad y buscas estructura."},
    7: {"nombre": "El Entusiasta", "herida": "Privación", "alas": [6, 8], 
        "rasgos": "Eres enérgico, saltas de un tema a otro, eres optimista y evitas temas dolorosos."},
    8: {"nombre": "El Desafiador", "herida": "Traición", "alas": [7, 9], 
        "rasgos": "Eres confrontativo, hablas con fuerza, no pides permiso y valoras la honestidad cruda."},
    9: {"nombre": "El Pacificador", "herida": "Negligencia", "alas": [8, 1], 
        "rasgos": "Eres pausado, evitas el conflicto, asientes mucho y tu lenguaje es muy suave."}
}

OCUPACIONES = {
    "infancia": ["Estudiante", "Chatarrero infantil", "Aprendiz de mecánica", "Mensajero de barrio"],
    "adolescencia": ["Estudiante", "Hacker novato", "Técnico de drones junior", "Recolector de datos"],
    "adulto": ["Minero de asteroides", "Científico de búnker", "Piloto de carga", "Ingeniero de sistemas", "Mercenario", "Agricultor hidropónico", "DJ de mercado negro"],
    "anciano": ["Mentor", "Archivista de lore", "Ingeniero retirado", "Ermitaño de la estación", "Ex-contrabandista"]
}

def generar_identidad_aleatoria():
    sexo = random.choice(["Masculino", "Femenino", "No binario"])
    edad = random.randint(8, 85)
    
    # Selección de nombre basada en sexo
    nombre = random.choice(NOMBRES_DB[sexo])
    
    if edad < 13: oc = random.choice(OCUPACIONES["infancia"])
    elif edad < 18: oc = random.choice(OCUPACIONES["adolescencia"])
    elif edad < 65: oc = random.choice(OCUPACIONES["adulto"])
    else: oc = random.choice(OCUPACIONES["anciano"])
    
    tipo_id = random.randint(1, 9)
    tipo_data = ENEAGRAMAS[tipo_id]
    
    return {
        "nombre_secreto": nombre,
        "sexo": sexo,
        "edad": edad,
        "ocupacion": oc,
        "eneatipo": f"{tipo_id}w{random.choice(tipo_data['alas'])}",
        "perfil_psicologico": tipo_data["nombre"],
        "herida_primaria": tipo_data["herida"],
        "instruccion_voz": tipo_data["rasgos"] # <--- LA CLAVE
    }
