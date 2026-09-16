import html
import streamlit as st

# Configuración general de la página
st.set_page_config(
    page_title="Asistente de Caracterización de Procesos",
    page_icon="🧭",
    layout="wide",
)

# Estilos sencillos para dar una apariencia limpia y profesional
st.markdown(
    """
    <style>
        .stApp { background-color: #f5f7fa; }
        .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
        h1, h2, h3 { color: #16324f; }
        .subtitle { color: #51606f; font-size: 1.08rem; margin-top: -0.7rem; margin-bottom: 1.5rem; }
        .section-card {
            background: white;
            border: 1px solid #dce3ea;
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 2px 8px rgba(22, 50, 79, 0.06);
            margin-bottom: 1rem;
        }
        .traffic {
            border-radius: 12px;
            padding: 1rem 1.2rem;
            color: white;
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0.5rem 0 1rem 0;
        }
        .green { background: #218838; }
        .yellow { background: #d39e00; }
        .red { background: #c82333; }
        .sipoc-card {
            background: white;
            border: 1px solid #d7e0e8;
            border-top: 5px solid #2f6f9f;
            border-radius: 12px;
            padding: 0.9rem;
            min-height: 170px;
            box-shadow: 0 2px 7px rgba(22, 50, 79, 0.06);
            overflow-wrap: anywhere;
        }
        .sipoc-title {
            color: #2f6f9f;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.04rem;
            margin-bottom: 0.55rem;
        }
        .arrow { text-align: center; color: #2f6f9f; font-size: 1.6rem; font-weight: 800; padding-top: 3.3rem; }
        .field-label { color: #2f6f9f; font-weight: 700; margin-bottom: 0.2rem; }
        .field-value { color: #293845; white-space: pre-wrap; overflow-wrap: anywhere; }
        div.stButton > button, div.stFormSubmitButton > button {
            border-radius: 9px;
            min-height: 3rem;
            font-weight: 700;
        }
        div.stFormSubmitButton > button {
            background: #1d5f91;
            color: white;
            border: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Campos del formulario y sus nombres visibles
FIELDS = {
    "nombre_proceso": "Nombre del proceso",
    "objetivo": "Objetivo del proceso",
    "responsable": "Responsable del proceso",
    "proveedor": "Proveedor",
    "entrada": "Entrada",
    "actividades": "Actividades principales",
    "salida": "Salida",
    "cliente": "Cliente o usuario",
    "criterio": "Criterio de aceptación de la salida",
    "indicador": "Indicador del proceso",
    "riesgos": "Riesgos u observaciones",
}


def safe_text(value):
    """Protege el texto antes de mostrarlo en bloques HTML."""
    text = str(value).strip() if value else ""
    return html.escape(text).replace("\n", "<br>") if text else "No diligenciado"


def clear_form():
    """Elimina los datos del formulario y el análisis guardado."""
    for key in list(FIELDS) + ["analysis_result"]:
        st.session_state.pop(key, None)


def show_field(label, value):
    """Muestra un campo de la ficha de forma uniforme."""
    st.markdown(
        f'<div class="section-card"><div class="field-label">{html.escape(label)}</div>'
        f'<div class="field-value">{safe_text(value)}</div></div>',
        unsafe_allow_html=True,
    )


# Encabezado
st.title("Asistente de Caracterización de Procesos")
st.markdown(
    '<p class="subtitle">Construya y revise de manera sencilla la caracterización de su proceso.</p>',
    unsafe_allow_html=True,
)

# Formulario principal
with st.form("process_form"):
    st.subheader("1. Información del proceso")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input(
            "Nombre del proceso *",
            key="nombre_proceso",
            placeholder="Ejemplo: Gestión de matrículas",
        )
        st.text_input(
            "Responsable del proceso",
            key="responsable",
            placeholder="Nombre, cargo o dependencia",
        )
        st.text_area(
            "Proveedor",
            key="proveedor",
            placeholder="Quién suministra la entrada",
            height=100,
        )
        st.text_area(
            "Entrada",
            key="entrada",
            placeholder="Información, solicitud o recurso recibido",
            height=110,
        )
        st.text_area(
            "Cliente o usuario",
            key="cliente",
            placeholder="Quién recibe o utiliza la salida",
            height=100,
        )
        st.text_area(
            "Indicador del proceso",
            key="indicador",
            placeholder="Ejemplo: porcentaje de matrículas procesadas a tiempo",
            height=100,
        )

    with col2:
        st.text_area(
            "Objetivo del proceso",
            key="objetivo",
            placeholder="Inicie con un verbo e indique qué se busca lograr",
            height=120,
        )
        st.text_area(
            "Actividades principales",
            key="actividades",
            placeholder="Escriba una actividad por línea",
            height=150,
        )
        st.text_area(
            "Salida",
            key="salida",
            placeholder="Producto, servicio, decisión o información generada",
            height=100,
        )
        st.text_area(
            "Criterio de aceptación de la salida",
            key="criterio",
            placeholder="Condición que debe cumplir la salida para ser aceptada",
            height=110,
        )
        st.text_area(
            "Riesgos u observaciones",
            key="riesgos",
            placeholder="Riesgos, controles, aclaraciones o notas relevantes",
            height=110,
        )

    analyzed = st.form_submit_button(
        "🔎 Analizar proceso",
        use_container_width=True,
        type="primary",
    )

# Botón independiente para iniciar una nueva ficha
st.button(
    "🧹 Limpiar formulario",
    on_click=clear_form,
    use_container_width=True,
)

# Procesamiento del formulario
if analyzed:
    current_data = {
        key: str(st.session_state.get(key, "")).strip()
        for key in FIELDS
    }

    if not any(current_data.values()):
        st.session_state.pop("analysis_result", None)
        st.warning("Debe diligenciar al menos algunos campos antes de analizar el proceso.")
    else:
        completed = sum(bool(value) for value in current_data.values())
        percentage = round((completed / len(FIELDS)) * 100)
        missing = [FIELDS[key] for key, value in current_data.items() if not value]
        st.session_state["analysis_result"] = {
            "data": current_data,
            "percentage": percentage,
            "missing": missing,
        }

# El resultado permanece visible hasta volver a analizar o limpiar
result = st.session_state.get("analysis_result")
if result:
    data = result["data"]
    percentage = result["percentage"]
    missing = result["missing"]

    st.divider()
    st.subheader("2. Resultado del análisis")
    st.metric("Completitud de la caracterización", f"{percentage} %")
    st.progress(percentage)

    # Semáforo según el nivel de completitud
    if percentage >= 80:
        traffic_class = "green"
        traffic_text = "🟢 VERDE – Caracterización completa"
    elif percentage >= 50:
        traffic_class = "yellow"
        traffic_text = "🟡 AMARILLO – Caracterización parcialmente completa"
    else:
        traffic_class = "red"
        traffic_text = "🔴 ROJO – Caracterización incompleta"

    st.markdown(
        f'<div class="traffic {traffic_class}">{traffic_text}</div>',
        unsafe_allow_html=True,
    )

    if missing:
        st.info("Campos pendientes por diligenciar:")
        for field in missing:
            st.markdown(f"- {field}")
    else:
        st.success("Todos los campos fueron diligenciados.")

    # Vista SIPOC en tarjetas. Los detalles del proceso combinan nombre y actividades.
    st.subheader("3. Visualización SIPOC")
    sipoc_items = [
        ("PROVEEDOR", data["proveedor"]),
        ("ENTRADA", data["entrada"]),
        (
            "PROCESO",
            "\n\n".join(
                part for part in [data["nombre_proceso"], data["actividades"]] if part
            ),
        ),
        ("SALIDA", data["salida"]),
        ("CLIENTE", data["cliente"]),
    ]

    # Alterna tarjetas y flechas para mostrar el flujo de izquierda a derecha.
    sipoc_columns = st.columns([1, 0.16, 1, 0.16, 1, 0.16, 1, 0.16, 1])
    column_index = 0
    for item_index, (title, value) in enumerate(sipoc_items):
        with sipoc_columns[column_index]:
            st.markdown(
                f'<div class="sipoc-card"><div class="sipoc-title">{title}</div>'
                f'<div class="field-value">{safe_text(value)}</div></div>',
                unsafe_allow_html=True,
            )
        column_index += 1
        if item_index < len(sipoc_items) - 1:
            with sipoc_columns[column_index]:
                st.markdown('<div class="arrow">→</div>', unsafe_allow_html=True)
            column_index += 1

    # Ficha resumen
    st.subheader("4. Resumen de la caracterización")
    summary_columns = st.columns(2)
    for index, (key, label) in enumerate(FIELDS.items()):
        with summary_columns[index % 2]:
            show_field(label, data[key])

    st.caption(
        "El porcentaje indica cuántos campos fueron diligenciados. "
        "No evalúa por sí solo la calidad técnica del contenido."
    )
