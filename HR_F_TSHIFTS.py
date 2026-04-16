# -*- coding: utf-8 -*-
from PY_FAC_ConexFactorial import * 
from datetime import *
from dateutil.relativedelta import relativedelta

    

def RUN_X_SHIFTS_UPDATE(opcion):
    
    """
    Actualiza la tabla X_SHIFTS obteniendo turnos desde la API de Factorial
    dentro de un rango de fechas determinado por la opción recibida.

    Parámetros
    ----------
    opcion : str
        Determina el rango temporal desde el cual comenzar la descarga de turnos.
        Valores posibles:
            - 'semana' : Usa el lunes de la semana pasada como fecha inicial.
            - 'mes'    : Usa el primer día del mes anterior.
            - 'year'   : Usa el día 1 de enero del año actual.
            - Cualquier otro valor : Usa la fecha por defecto '2023-10-01'.

    Descripción
    -----------
    La función:
        1. Calcula la fecha inicial (`start_on`) según la opción indicada.
        2. Define la fecha final (`end_on`) como la fecha actual.
        3. Llama a la API de Factorial para obtener turnos paginados.
        4. Para cada turno:
            - Valida datos nulos.
            - Convierte horas de clock_in y clock_out a objetos datetime.time.
            - Calcula la diferencia de tiempo trabajada y los minutos totales.
        5. Inserta o actualiza los registros en la tabla MySQL `X_SHIFTS`
           mediante un `INSERT IGNORE ... ON DUPLICATE KEY UPDATE`.
        6. Continúa recorriendo páginas si existe `@odata.nextLink`.

    Efectos secundarios
    -------------------
    - Escribe registros en la base de datos MySQL.
    - Imprime en consola el progreso y posibles errores.
    - Realiza solicitudes HTTPS a la API de Factorial.

    Notas
    -----
    - Solo procesa turnos con `clock_out` no nulo.
    - Maneja turnos que cruzan medianoche para cálculo correcto de horas.
    - `headers_factorial` y `connection` deben estar configurados globalmente.

    Retorno
    -------
    None
        La función no devuelve valores; su propósito es procesamiento e inserción
        de datos.
    """
    
    print("RUN X_SHIFTS_UPDATE")

    # Calcular el primer día del mes actual y del último mes
    hoy = datetime.today()
    primer_dia_mes_actual = hoy.replace(day=1)
    ultimo_mes = primer_dia_mes_actual - timedelta(days=1)
    ultimo_dia_mes_anterior = primer_dia_mes_actual - timedelta(days=1)
    primer_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)
    
    lunes_actual = hoy - timedelta(days=hoy.weekday())
    print(lunes_actual)
    
    semana_pasada = (lunes_actual - timedelta(weeks=1)).strftime('%Y-%m-%d')
    
    last_year = datetime(hoy.year, 1, 1).strftime('%Y-%m-%d')
    
    match opcion:
        case 'semana':
            start_on = semana_pasada
        case 'mes':
            start_on = primer_dia_mes_anterior.strftime('%Y-%m-%d')
        case 'year':
            start_on = last_year
        case _:
            start_on = '2023-10-01'
            
    end_on = hoy.strftime('%Y-%m-%d')

    print(f"Obteniendo turnos de: {start_on} hasta {end_on}")

    url = f"https://api.factorialhr.com/api/2025-04-01/resources/attendance/shifts?half_day=false&sort_created_at_asc=true&start_on={start_on}&end_on={end_on}"
    nombre_tabla = "X_SHIFTS"
    salida = "no"
    entero = 0
    cursor = connection.cursor()

    while True:
        respuesta = requests.get(url, headers=headers_factorial)

        if respuesta.status_code == 200:
            json_data = respuesta.json()
            entero += 1

            if json_data:
                for entry in json_data["data"]:
                    if entry["clock_out"] is not None:
                        try:
                            XF_TS_id = entry["id"]
                            XF_TS_date = entry["date"]
                            XF_TS_clock_in_str = entry["clock_in"]
                            XF_TS_clock_out_str = entry["clock_out"]
                            XF_TS_employee_id = entry["employee_id"]
                            XF_TS_observations = entry["observations"]
                            XF_TS_workable = entry["workable"]

                            # Validar nulos
                            if XF_TS_clock_in_str is None:
                                XF_TS_clock_in_str = "00:00"

                            XF_TS_clock_in = datetime.strptime(XF_TS_clock_in_str, '%H:%M').time()
                            XF_TS_clock_out = datetime.strptime(XF_TS_clock_out_str, '%H:%M').time()

                            # Calcular diferencia
                            if XF_TS_clock_out >= XF_TS_clock_in:
                                XF_TS_Timediff = datetime.combine(datetime.min, XF_TS_clock_out) - datetime.combine(datetime.min, XF_TS_clock_in)
                            else:
                                XF_TS_Timediff = datetime.combine(datetime.min, XF_TS_clock_out) + timedelta(days=1) - datetime.combine(datetime.min, XF_TS_clock_in)

                            XF_TS_minutos = round(XF_TS_Timediff.total_seconds() / 60, 2)

                            values = (
                                XF_TS_id,
                                XF_TS_date,
                                XF_TS_clock_in,
                                XF_TS_clock_out,
                                XF_TS_employee_id,
                                XF_TS_observations,
                                XF_TS_workable,
                                XF_TS_Timediff,
                                XF_TS_minutos
                            )

                            query = f"""
                            INSERT IGNORE INTO {nombre_tabla} (
                                XF_TS_id,
                                XF_TS_Date_Value,
                                XF_TS_clock_in,
                                XF_TS_clock_out,
                                XF_TS_employee_id,
                                XF_TS_observations,
                                XF_TS_workable,
                                XF_TS_Timediff,
                                XF_TS_minutos
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                XF_TS_Date_Value = VALUES(XF_TS_Date_Value),
                                XF_TS_clock_in = VALUES(XF_TS_clock_in),
                                XF_TS_clock_out = VALUES(XF_TS_clock_out),
                                XF_TS_employee_id = VALUES(XF_TS_employee_id),
                                XF_TS_observations = VALUES(XF_TS_observations),
                                XF_TS_workable = VALUES(XF_TS_workable),
                                XF_TS_Timediff = VALUES(XF_TS_Timediff),
                                XF_TS_minutos = VALUES(XF_TS_minutos)
                            """
                            cursor.execute(query, values)
                            connection.commit()
                            print(f"Turno procesado: ID {XF_TS_id}")

                        except Exception as e:
                            print(f"Error al procesar turno: {e}")
                        
                if "@odata.nextLink" in json_data:
                    url = json_data["@odata.nextLink"]
                    print("Cargando siguiente página de resultados...")
                else:
                    print("Todos los turnos procesados.")
                    break
            else:
                print("No se recibieron datos JSON.")
                break
        else:
            print(f"Error en la solicitud: {respuesta.status_code}")
            break



RUN_X_SHIFTS_UPDATE('a')
#RUN_X_SHIFTS("a")      


