from flask import Flask, render_template_string, request
from calculadora_salarial import calcular_ajuste_salarial_petrolera, CATALOGO_CARGOS

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>MAG - Finanzas Petroleras</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f4f4f6; 
            color: #2b2d42; 
            padding: 30px; 
            margin: 0;
        }
        .container { 
            max-width: 680px; 
            margin: auto; 
            background: #ffffff; 
            padding: 35px; 
            border-radius: 12px; 
            box-shadow: 0 4px 20px rgba(43, 45, 66, 0.08); 
            border: 1px solid #e2e8f0;
        }
        h1 { 
            color: #1e293b; 
            text-align: center; 
            margin-bottom: 5px;
            font-size: 24px;
        }
        .subtitle {
            text-align: center;
            color: #64748b;
            font-size: 14px;
            margin-bottom: 25px;
            font-weight: 500;
        }
        .section-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        label { 
            display: block; 
            margin-top: 12px; 
            font-weight: 600; 
            color: #475569;
            font-size: 13px;
        }
        input, select { 
            width: 100%; 
            padding: 10px; 
            margin-top: 5px; 
            border-radius: 6px; 
            border: 1px solid #cbd5e1; 
            background: #ffffff; 
            color: #1e293b; 
            box-sizing: border-box; 
            font-size: 14px;
        }
        .checkbox-container {
            display: flex;
            align-items: center;
            margin-top: 15px;
        }
        .checkbox-container input {
            width: 20px;
            height: 20px;
            margin-right: 10px;
        }
        button { 
            width: 100%; 
            margin-top: 25px; 
            padding: 14px; 
            background: #334155; 
            color: white; 
            border: none; 
            border-radius: 6px; 
            font-size: 16px; 
            cursor: pointer; 
            font-weight: 600; 
            transition: background 0.2s;
        }
        button:hover { 
            background: #1e293b; 
        }
        .result { 
            margin-top: 30px; 
            background: #f8fafc; 
            padding: 22px; 
            border-radius: 8px; 
            border: 1px solid #e2e8f0;
            border-left: 5px solid #334155; 
        }
        .result h3 { 
            margin-top: 0; 
            color: #1e293b; 
            font-size: 18px;
        }
        .result p {
            margin: 6px 0;
            color: #334155;
            font-size: 14px;
        }
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
            <input type="number" name="anos_antiguedad" required value="{{ request.form.get('anos_antiguedad', 2) }}">
            
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
            <input type="number" step="0.1" name="porcentaje_inflacion" required value="{{ request.form.get('porcentaje_inflacion', 10) }}">
            
            <label>Índice de Competitividad del Mercado Petrolero:</label>
            <input type="number" step="0.01" name="indice_competitividad" required value="{{ request.form.get('indice_competitividad', 1.05) }}">

            <label>Entorno u Ubicación Operativa del Puesto:</label>
            <select name="factor_riesgo_operativo">
                <option value="oficina" {% if entorno_seleccionado == 'oficina' %}selected{% endif %}>Oficina</option>
                <option value="directivo" {% if entorno_seleccionado == 'directivo' %}selected{% endif %}>Directivo</option>
                <option value="operativo_campo" {% if entorno_seleccionado == 'operativo_campo' or not entorno_seleccionado %}selected{% endif %}>Operativo en campo</option>
            </select>

            <div class="checkbox-container">
                <input type="checkbox" id="hse" name="tiene_certificacion_hse" {% if request.form.get('tiene_certificacion_hse') %}checked{% endif %}>
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
    
    if request.method == "POST":
        try:
            cargo_seleccionado = request.form["cargo_clave"]
            salario_base_val = float(request.form["salario_base"])
            antiguedad = int(request.form["anos_antiguedad"])
            nivel_seleccionado = request.form["nivel_profesionalismo"]
            inflacion = float(request.form["porcentaje_inflacion"])
            competitividad = float(request.form["indice_competitividad"])
            entorno_seleccionado = request.form["factor_riesgo_operativo"]
            hse = True if request.form.get("tiene_certificacion_hse") else False
            
            resultado = calcular_ajuste_salarial_petrolera(
                cargo_seleccionado, salario_base_val, antiguedad, nivel_seleccionado, inflacion, competitividad, entorno_seleccionado, hse
            )
        except Exception as e:
            print("Error en cálculo:", e)
            
    return render_template_string(
        HTML_TEMPLATE, 
        resultado=resultado, 
        catalogo=CATALOGO_CARGOS, 
        cargo_seleccionado=cargo_seleccionado,
        nivel_seleccionado=nivel_seleccionado,
        entorno_seleccionado=entorno_seleccionado,
        salario_base_val=salario_base_val
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)