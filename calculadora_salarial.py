# Catálogo completo de cargos petroleros y salarios base de referencia
CATALOGO_CARGOS = {
    "supervisor_campo": {"titulo": "Supervisor de Campo", "base": 400.0},
    "supervisor_soldadura": {"titulo": "Supervisor de Soldadura", "base": 450.0},
    "supervisor_electrico": {"titulo": "Supervisor Eléctrico", "base": 450.0},
    "supervisor_mecanico": {"titulo": "Supervisor Mecánico", "base": 450.0},
    "supervisor_operaciones_turno": {"titulo": "Supervisor de Operaciones de Turno", "base": 480.0},
    "supervisor_laboral": {"titulo": "Supervisor Laboral", "base": 420.0},
    "jefe_equipo": {"titulo": "Jefe de Equipo", "base": 550.0},
    "superintendente": {"titulo": "Superintendente", "base": 750.0}
}

def calcular_ajuste_salarial_petrolera(
    cargo_clave,
    salario_base_custom,
    anos_antiguedad,
    nivel_profesionalismo,
    porcentaje_inflacion,
    indice_competitividad,
    factor_riesgo_operativo,
    tiene_certificacion_hse
):
    # Si el usuario ingresó un salario personalizado, lo usa; si no, toma el del catálogo
    salario_base = salario_base_custom if salario_base_custom > 0 else CATALOGO_CARGOS.get(cargo_clave, {"base": 400.0})["base"]
    
    # 1. Ajuste por Inflación
    monto_inflacion = salario_base * (porcentaje_inflacion / 100)
    
    # 2. Bono por Antigüedad (2% anual acumulativo)
    factor_antiguedad = 0.02
    monto_antiguedad = salario_base * (anos_antiguedad * factor_antiguedad)
    
    # 3. Multiplicador por Nivel Académico / Profesional
    pesos_profesionalismo = {
        'tsu': 1.05,
        'licenciado': 1.10,
        'ingeniero': 1.15,
        'medico': 1.18,
        'abogado': 1.12,
        'bachiller': 1.00
    }
    mult_prof = pesos_profesionalismo.get(nivel_profesionalismo.lower(), 1.0)
    
    salario_parcial = (salario_base + monto_inflacion + monto_antiguedad) * mult_prof
    
    # 4. Ajuste por Competitividad de Mercado
    salario_competitivo = salario_parcial * indice_competitividad
    
    # 5. Componentes Industriales / Entorno Operativo
    # Asignación de porcentaje de riesgo según la nueva clasificación
    adicionales_riesgo = {
        'oficina': 0.02,       # 2% de asignación administrativa
        'directivo': 0.05,     # 5% de responsabilidad ejecutiva
        'operativo_campo': 0.10 # 10% de riesgo e exposición directa en locación
    }
    adicional_riesgo = adicionales_riesgo.get(factor_riesgo_operativo.lower(), 0.03)
    monto_riesgo = salario_competitivo * adicional_riesgo
    
    monto_hse = (salario_base * 0.05) if tiene_certificacion_hse else 0.0
    
    salario_final = salario_competitivo + monto_riesgo + monto_hse
    
    # Diccionarios legibles para el reporte final
    titulos_academicos = {
        'tsu': 'Técnico Superior Universitario (TSU)',
        'licenciado': 'Licenciado',
        'ingeniero': 'Ingeniero',
        'medico': 'Médico',
        'abogado': 'Abogado',
        'bachiller': 'Bachiller en Ciencias'
    }
    
    titulos_entorno = {
        'oficina': 'Oficina (Administrativo)',
        'directivo': 'Directivo / Ejecutivo',
        'operativo_campo': 'Operativo en Campo (Locación)'
    }
    
    resultado = {
        "cargo_seleccionado": CATALOGO_CARGOS.get(cargo_clave, {"titulo": "Personal de Campo"}).get("titulo"),
        "nivel_academico": titulos_academicos.get(nivel_profesionalismo.lower(), 'No especificado'),
        "entorno_operativo": titulos_entorno.get(factor_riesgo_operativo.lower(), 'No especificado'),
        "salario_base": round(salario_base, 2),
        "ajuste_inflacion": round(monto_inflacion, 2),
        "bono_antiguedad": round(monto_antiguedad, 2),
        "bono_entorno_laboral": round(monto_riesgo, 2),
        "bono_hse": round(monto_hse, 2),
        "salario_ajustado": round(salario_final, 2),
        "incremento_neto": round(salario_final - salario_base, 2),
        "porcentaje_total_aumento": round(((salario_final - salario_base) / salario_base) * 100, 2)
    }
    
    return resultado

if __name__ == "__main__":
    prueba = calcular_ajuste_salarial_petrolera(
        cargo_clave='supervisor_campo',
        salario_base_custom=400.0,
        anos_antiguedad=3,
        nivel_profesionalismo='ingeniero',
        porcentaje_inflacion=10.0,
        indice_competitividad=1.05,
        factor_riesgo_operativo='operativo_campo',
        tiene_certificacion_hse=True
    )
    print("--- SIMULACIÓN MAG ---")
    for k, v in prueba.items():
        print(f"{k}: {v}")