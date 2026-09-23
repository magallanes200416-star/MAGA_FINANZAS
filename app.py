import os
from flask import Flask, render_template_string, request

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
    salario_base = salario_base_custom if salario_base_custom > 0 else CATALOGO_CARGOS.get(cargo_clave, {"base": 400.0})["base"]
    
    monto_inflacion = salario_base * (porcentaje_inflacion / 100)
    
    factor_antiguedad = 0.02
    monto_antiguedad = salario_base * (anos_antiguedad * factor_antiguedad)
    
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
    salario_competitivo = salario_parcial * indice_competitividad
    
    adicionales_riesgo = {
        'oficina': 0.02,
        'directivo': 0.05,
        'operativo_campo': 0.10
    }
    adicional_riesgo = adicionales_riesgo.get(factor_riesgo_operativo.lower(), 0.03)
    monto_riesgo = salario_competitivo * adicional_riesgo
    
    monto_hse = (salario_base * 0.05) if tiene_certificacion_hse else 0.0
    salario_final = salario_competitivo + monto_riesgo + monto_hse
    
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

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>MAG - Finanzas Petroleras</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f4f6; color: #2b2d42; padding: 30px; margin: 0; }
        .container { max-width: 680px; margin: auto; background: #ffffff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 20px rgba(43, 45, 66, 0.08); border: 1px solid #e2e8f0; }
        h1 { color: #1e293b; text-align: center; margin-bottom: 5px; font-size: 24px; }
        .subtitle { text-align: center; color: #64748b; font-size: 14px; margin-bottom: 25px; font-weight: 500; }
        .section-box { background: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        label { display: block; margin-top: 12px; font-weight: 600; color: #475569; font-size: 13px; }
        input, select { width: 100%; padding: 10px; margin-top: 5px; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #1e293b; box-sizing: border-box; font-size: 14px; }
        .checkbox-container { display: flex; align-items: center; margin-top: 15px; }
        .checkbox-container input { width: 20px; height: 20px; margin-right: 10px; }
        button { width: 100%; margin-top: 25px; padding: 14px; background: #334155; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; font-weight: 600; transition: background 0.2s; }
        button:hover { background: #1e293b; }
        .result { margin-top: 30px; background: #f8fafc; padding: 22px; border-radius: 8px; border: 1px solid #e2e8f0; border-left: 5px solid #334155; }
        .result h3 { margin-top: 0; color: #1e293b; font-size: 18px; }
        .result p { margin: 6px 0; color: #334155; font-size: 14px; }
    </style>
    <script>
        const basesCargos = {
            {% for clave, info in catalogo.items() %}
            "{{ clave }}": {{ info.base }},
            {% endfor %}
        };
        function actualizarSalarioBase() {
            const selectCargo = document.getElementById("cargo_clave");
            const inputSalario = document.getElementById("salario_base");
            const cargoSeleccionado = selectCargo.value;
            if (basesCargos[cargoSeleccionado] !== undefined) {
                inputSalario.value = basesCargos[cargoSeleccionado];
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>MAG — Operadora Petrolera Independiente</h1>
        <div class="subtitle">Sistema Local de Compensación y Ajuste Salarial de Campo</div>
        
        <form method="POST">
            <div class="section-box">
                <label style="margin-top: 0; color: #1e293b; font-size: 15px;">Selección Principal de Cargo Laboral en Campo:</label>
                <select name="cargo_clave" id="cargo_clave" onchange="actualizarSalarioBase()" style="margin-top: 8px; font-weight: bold;">
                    {% for clave, info in catalogo.items() %}
                    <option value="{{ clave }}" {% if cargo_seleccionado == clave %}selected{% endif %}>
                        {{ info.titulo }} (Base sugerida: ${{ info.base }})
                    </option>
                    {% endfor %}
                </select>

                <label>Salario Base Automático / Referencia ($) [Editable]:</label>
                <input type="number" step="0.01" id="salario_base" name="salario_base" required value="{{ salario_base_val }}">
            </div>
            
            <label>Años de Antigüedad:</label>
            <input type="number" name="anos_antiguedad" required value="{{ anos_val }}">
            
            <label>Nivel Profesional / Académico:</label>
            <select name="nivel_profesionalismo">
                <option value="tsu" {% if nivel_seleccionado == 'tsu' %}selected{% endif %}>Técnico Superior Universitario (TSU)</option>
                <option value="licenciado" {% if nivel_seleccionado == 'licenciado' %}selected{% endif %}>Licenciado</option>
                <option value="ingeniero" {% if nivel_seleccionado == 'ingeniero' %}selected{% endif %}>Ingeniero</option>
                <option value="medico" {% if nivel_seleccionado == 'medico' %}selected{% endif %}>Médico</option>
                <option value="abogado" {% if nivel_seleccionado == 'abogado' %}selected{% endif %}>Abogado</option>
                <option value="bachiller" {% if nivel_seleccionado == 'bachiller' %}selected{% endif %}>Bachiller en Ciencias</option>
            </select>
            
            <label>Inflación Anual Estimada (%):</label>
            <input type="number" step="0.1" name="porcentaje_inflacion" required value="{{ inflacion_val }}">
            
            <label>Índice de Competitividad del Mercado Petrolero:</label>
            <input type="number" step="0.01" name="indice_competitividad" required value="{{ competitividad_val }}">

            <label>Entorno u Ubicación Operativa del Puesto:</label>
            <select name="factor_riesgo_operativo">
                <option value="oficina" {% if entorno_seleccionado == 'oficina' %}selected{% endif %}>Oficina</option>
                <option value="directivo" {% if entorno_seleccionado == 'directivo' %}selected{% endif %}>Directivo</option>
                <option value="operativo_campo" {% if entorno_seleccionado == 'operativo_campo' %}selected{% endif %}>Operativo en campo</option>
            </select>

            <div class="checkbox-container">
                <input type="checkbox" id="hse" name="tiene_certificacion_hse" {% if hse_val %}checked{% endif %}>
                <label for="hse" style="margin-top: 0; display: inline; cursor: pointer;">Posee Certificaciones HSE / Especializadas Vigentes</label>
            </div>
            
            <button type="submit">Calcular Ajuste Salarial Completo</button>
        </form>

        {% if resultado %}
        <div class="result">
            <h3>Desglose Salarial: {{ resultado.cargo_seleccionado }}</h3>
            <p><strong>Nivel Académico:</strong> {{ resultado.nivel_academico }}</p>
            <p><strong>Entorno Operativo:</strong> {{ resultado.entorno_operativo }}</p>
            <p><strong>Salario Base Aplicado:</strong> ${{ resultado.salario_base }}</p>
            <p><strong>Ajuste por Inflación:</strong> +${{ resultado.ajuste_inflacion }}</p>
            <p><strong>Bono por Antigüedad:</strong> +${{ resultado.bono_antiguedad }}</p>
            <p><strong>Asignación por Entorno Laboral:</strong> +${{ resultado.bono_entorno_laboral }}</p>
            <p><strong>Bono Certificación HSE:</strong> +${{ resultado.bono_hse }}</p>
            <p><strong>Salario Ajustado Final:</strong> ${{ resultado.salario_ajustado }}</p>
            <p><strong>Incremento Neto Total:</strong> +${{ resultado.incremento_neto }} (<strong>{{ resultado.porcentaje_total_aumento }}%</strong>)</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    cargo_seleccionado = "supervisor_campo"
    nivel_seleccionado = "ingeniero"
    entorno_seleccionado = "operativo_campo"
    salario_base_val = CATALOGO_CARGOS["supervisor_campo"]["base"]
    anos_val = 2
    inflacion_val = 10.0
    competitividad_val = 1.05
    hse_val = False
    
    if request.method == "POST":
        try:
            cargo_seleccionado = request.form.get("cargo_clave", "supervisor_campo")
            
            raw_salario = request.form.get("salario_base", "")
            salario_base_val = float(raw_salario) if raw_salario else CATALOGO_CARGOS.get(cargo_seleccionado, {"base": 400.0})["base"]
            
            anos_val = int(request.form.get("anos_antiguedad", 2) or 2)
            nivel_seleccionado = request.form.get("nivel_profesionalismo", "ingeniero")
            inflacion_val = float(request.form.get("porcentaje_inflacion", 10.0) or 10.0)
            competitividad_val = float(request.form.get("indice_competitividad", 1.05) or 1.05)
            entorno_seleccionado = request.form.get("factor_riesgo_operativo", "operativo_campo")
            hse_val = True if request.form.get("tiene_certificacion_hse") else False
            
            resultado = calcular_ajuste_salarial_petrolera(
                cargo_seleccionado, salario_base_val, anos_val, nivel_seleccionado, 
                inflacion_val, competitividad_val, entorno_seleccionado, hse_val
            )
        except Exception as e:
            print("Aviso de error controlado en cálculo:", e)
            resultado = None
            
    return render_template_string(
        HTML_TEMPLATE, 
        resultado=resultado, 
        catalogo=CATALOGO_CARGOS, 
        cargo_seleccionado=cargo_seleccionado,
        nivel_seleccionado=nivel_seleccionado,
        entorno_seleccionado=entorno_seleccionado,
        salario_base_val=salario_base_val,
        anos_val=anos_val,
        inflacion_val=inflacion_val,
        competitividad_val=competitividad_val,
        hse_val=hse_val
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)