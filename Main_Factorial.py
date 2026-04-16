#_*_ coding: utf-8 _*_
from HR_FACTORIAL_CONTRACTS import RUN_CONTRACTS
from HR_FACTORIAL_EMPLOYEES import RUN_EMPLOYEES
from HR_F_APPLICATION import RUN_APPLICATION
from HR_F_APPLICATION_PHASES import RUN_APPLICATION_PHASES
from HR_F_CANDIDATES import RUN_CANDIDATES
from HR_F_CATEGORIES import RUN_CATEGORIES
from HR_F_CONTRACT_TYPES import RUN_CONTRACT_TYPES
from HR_F_DAY_CONFIGURATION import RUN_DAY
from HR_F_EDUCATION_LEVEL import RUN_EDUCATION_LEVEL
from HR_F_ESTIMATED_TIME import RUN_ESTIMATED
from HR_F_HOLIDAYS import RUN_HOLIDAYS
from HR_F_LEAVES import RUN_LEAVES
from HR_F_LEVEL import RUN_LEVELS
from HR_F_PLANNING import RUN_PLANNING
from HR_F_SCHEDULE import RUN_SCHEDULE
from HR_F_SESSIONS import RUN_SESSIONS
from HR_F_SESSION_ATTENDANCE import RUN_SESSION_ATTENDANCE
from HR_F_SPANISH_PROFESSIONAL_CATEGORY import RUN_PROFESSIONAL_CATEGORIES
from HR_F_TEAMSMEMBER import RUN_TEAMSMEMBER
from HR_F_TRAININGS import RUN_TRAININGS
# from HR_FACTORIAL_LOCATION import RUN_LOCATION
from HR_FACTORIAL_TEAMS import main
from HR_F_TSHIFTS import RUN_X_SHIFTS,RUN_X_SHIFTS_UPDATE



def ejecutar_seguro(funcion, nombre, *args):
   
    try:
        if args:
            funcion(*args)
        else:
            funcion()
        print(f"{nombre}: Completado con exito")
    except Exception as e:
        print(f"Error en {nombre}: {e}")

# Definimos la lista de tareas: (función, nombre_para_log, argumentos_si_los_hay)
tareas = [
    (RUN_CONTRACTS, "HR_F_CONTRACTS"),
    (RUN_EMPLOYEES, "HR_F_EMPLOYEES", "ad"),
    (RUN_APPLICATION, "HR_F_APPLICATION"),
    (RUN_APPLICATION_PHASES, "HR_F_APPLICATION_PHASES"),
    (RUN_CANDIDATES, "HR_F_CANDIDATES"),
    (RUN_CATEGORIES, "HR_F_CATEGORIES"),
    (RUN_LEVELS, "HR_F_LEVELS", "ad"),
    (RUN_SESSIONS, "HR_F_SESSIONS"),
    (RUN_SESSION_ATTENDANCE, "HR_F_SESSION_ATTENDANCE"),
    (RUN_PROFESSIONAL_CATEGORIES, "HR_F_PROFESSIONAL_CATEGORIES"),
    (RUN_TRAININGS, "HR_F_TRAININGS"),
    (RUN_CONTRACT_TYPES, "HR_F_CONTRACT_TYPES"),
    (RUN_EDUCATION_LEVEL, "HR_F_EDUCATION_LEVEL"),
    (RUN_TEAMSMEMBER, "HR_F_TEAMSMEMBER"),
    (main, "HR_F_FACTORIAL_TEAMS"),
    # Para RUN_X_SHIFTS_UPDATE hay 3 opciones:
    # semana: Devuelve las horas fichadas de todos los empleados de la ultima semana
    # mes: Devuelve las horas fichadas de todos los empleados del ultimo mes
    # year: Devuelve las horas fichadas de todos los empleados del ultimo año
    (RUN_X_SHIFTS_UPDATE, "X_SHIFTS", "semana"),
    (RUN_HOLIDAYS, "HR_F_HOLIDAYS"),
    (RUN_LEAVES, "HR_F_LEAVES"),
    (RUN_SCHEDULE, "HR_F_SCHEDULE"),
    (RUN_DAY, "HR_F_DAY_CONFIGURATION"),
    # Para RUN_ESTIMATED hay 3 opciones:
    # semana: Devuelve las horas planificadas de todos los empleados de la ultima semana
    # mes: Devuelve las horas planificadas de todos los empleados del ultimo mes
    # year: Devuelve las horas planificadas de todos los empleados del ultimo año
    (RUN_ESTIMATED, "HR_F_ESTIMATED_TIME", "semana"),
    (RUN_PLANNING, "HR_F_PLANNING")
]


if __name__ == "__main__":
    print("Iniciando ejecucion de procesos HR...\n")
    for tarea in tareas:
        func = tarea[0]
        nombre = tarea[1]
        argumentos = tarea[2:] # Coge todos los argumentos extra si existen
        
        ejecutar_seguro(func, nombre, *argumentos)
    
    print("\nFinalizado el proceso de carga.")
