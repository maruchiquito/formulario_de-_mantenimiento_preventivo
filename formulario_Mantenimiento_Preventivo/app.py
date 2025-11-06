import os
import pandas as pd
import streamlit as st
from datetime import datetime
import json
from datetime import date, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Table, TableStyle, Paragraph, Spacer, KeepTogether
)
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, KeepTogether, PageBreak
from reportlab.lib import colors
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def bloque_observaciones_pdf(observaciones_texto):
    elems = [
        PageBreak(),
        Paragraph("OBSERVACIONES GENERALES", styles["Heading2"]),
        Spacer(1, 6)
    ]

    
    data = [
        ["Observaciones Generales", Paragraph(str(observaciones_texto or ""), styles["Normal"])]
    ]

    # Tabla con bordes y ajuste de texto
    tabla = Table(data, colWidths=[150, 350])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#97c6e9")),  # Encabezado azul
        ("TEXTCOLOR", (0, 0), (0, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),  # Ajuste de texto largo
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))

    elems.append(tabla)
    elems.append(Spacer(1, 10))
    return KeepTogether(elems)



# ============================================================
# 🧾 CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Mantenimiento Preventivo",
    page_icon="icono.ico.png",  
    layout="wide"
)



styles = getSampleStyleSheet()

cell_style = ParagraphStyle(
    name="cell_style",
    fontSize=9,
    leading=10,
    alignment=0,      # Izquierda
)

obs_style = ParagraphStyle(
    name="obs_style",
    fontSize=9,
    leading=10,
    alignment=0       # Izquierda
)

# ============================================================
# 🖼️ ENCABEZADO CON LOGO Y TÍTULO
# ============================================================

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    # ================================
# RUTAS DE IMÁGENES
# ================================
 from pathlib import Path



BASE_DIR = Path(__file__).parent

logo_path = BASE_DIR / "logo_claro.png"
uso_interno_path = BASE_DIR / "uso_interno.png"
banner_path = BASE_DIR / "img.png"
icono_path = BASE_DIR / "icono.ico.png"

# Configuración de página con ícono
st.set_page_config(
    page_title="Mantenimiento Preventivo",
    page_icon=str(icono_path) if icono_path.exists() else None,
    layout="wide"
)

# Mostrar logo
if logo_path.exists():
    st.image(str(logo_path), width=180)
else:
    st.warning("⚠️ No se encontró el archivo logo_claro.png")


st.markdown("""
    <h1 style='text-align:center; color:#004080;'>🧰 FORMATO DE MANTENIMIENTO PREVENTIVO</h1>
    <h4 style='text-align:center; color:gray;'>Sistema de Gestión de Mantenimiento - Área de Operaciones</h4>
""", unsafe_allow_html=True)



# CSS ligero para móvil y apariencia
st.markdown("""
    <style>
    @media (max-width: 600px) {
        .block-container { padding-left: 0.6rem; padding-right: 0.6rem; }
    }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #0b5ed7; color: white; font-weight: 600; }
    .stDownloadButton>button { width: 100%; border-radius: 6px; background-color: #198754; color: white; font-weight: 600; }
    .reportview-container .main .block-container{ max-width: 980px; padding-top: 1rem; }
    </style>
""", unsafe_allow_html=True)


# Encabezado PDF (logos y franja uso_interno con margen 15)

def header_canvas(canvas, doc):
    canvas.saveState()
    width, height = A4

    if os.path.exists("logo_claro.png"):
        try:
            canvas.drawImage("logo_claro.png", 50, height-70, width=100, height=60, preserveAspectRatio=True, mask='auto')
        except:
            pass
    else:
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(30, height-40, "LOGO CLARO")

   
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(width / 2, height - 40, "FORMATO DE MANTENIMIENTO PREVENTIVO")
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(width / 2, height - 55, "ACCESO ")
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(width / 2, height - 70, "OT / Registro")

    # Franja uso_interno con margen 15
    if os.path.exists("uso_interno.png"):
        try:
            canvas.drawImage("uso_interno.png", 20, height - 100, width=width - 30, height=30, preserveAspectRatio=False, mask='auto')
        except:
            canvas.setFillColorRGB(0.9, 0.9, 0.9)
            canvas.rect(15, height - 100, width - 30, 20, fill=1, stroke=0)
            canvas.setFillColorRGB(0, 0, 0)
            canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(width / 2, height - 95, "USO INTERNO")
    else:
        canvas.setFillColorRGB(0.9, 0.9, 0.9)
        canvas.rect(15, height - 100, width - 30, 20, fill=1, stroke=0)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont("Helvetica", 8)
        canvas.drawCentredString(width / 2, height - 95, "USO INTERNO")

    canvas.restoreState()

def fecha_hora_actual():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def estilo_tabla_basico():
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ])


def crear_tabla(data, col_widths=None, repeat_header=True):
    """
    Crea una tabla con estilo uniforme y ajuste de texto.
    Compatible con los estilos actuales de la app.
    """
    if col_widths is None:
        col_widths = [260, 260]  # ancho por defecto

    tabla = Table(data, colWidths=col_widths, repeatRows=1 if repeat_header else 0)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),  
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),   # texto arriba
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),   # texto a la izquierda
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),  # evita desbordamiento de texto
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    return tabla




def df_to_table_data(df):
   
    if df is None or df.empty:
        return []
    cols = list(df.columns)
    data = [cols]
    for _, row in df.iterrows():
        data.append([str(row[c]) if not pd.isna(row[c]) else "" for c in cols])
    return data


def bloque_informacion_general(datos):
    elems = []
    elems.append(Paragraph(" INFORMACIÓN GENERAL", styles['Heading2']))

    data = [["DESCRIPCIÓN", "OBSERVACIÓN"]]
    for k, v in datos.items():
        data.append([Paragraph(str(k), styles["Normal"]), Paragraph(str(v or ""), styles["Normal"])])

    tabla = Table(data, colWidths=[250, 270])
    tabla.setStyle(estilo_tabla_basico())

    elems.append(tabla)
    elems.append(Spacer(1, 8))
    return KeepTogether(elems)

def bloque_actividades_pdf(datos):
    elems = []
    elems.append(Paragraph(" ACTIVIDADES", styles['Heading2']))
    data = [["Actividad", "Estado"]]
    for k, v in datos.items():
        data.append([k, v])
    elems.append(crear_tabla(data))
    elems.append(Spacer(1,8))
    return KeepTogether(elems)


def bloque_tdg_pdf(datos):
    elems = []
    elems.append(Paragraph(" TDG", styles['Heading2']))

    data = [["DESCRIPCIÓN", "OBSERVACIÓN"]]
    for k, v in datos.items():
        data.append([Paragraph(str(k), styles["Normal"]), Paragraph(str(v or ""), styles["Normal"])])

    tabla = Table(data, colWidths=[250, 270])
    tabla.setStyle(estilo_tabla_basico())

    elems.append(tabla)
    elems.append(Spacer(1, 8))
    return KeepTogether(elems)

def bloque_spt_pdf(datos):
    elems = []
    elems.append(Paragraph(" SPT", styles['Heading2']))

    data = [["DESCRIPCIÓN", "OBSERVACIÓN"]]
    for k, v in datos.items():
        data.append([Paragraph(str(k), styles["Normal"]), Paragraph(str(v or ""), styles["Normal"])])

    tabla = Table(data, colWidths=[250, 270])
    tabla.setStyle(estilo_tabla_basico())

    elems.append(tabla)
    elems.append(Spacer(1, 14))
    return KeepTogether(elems)

def bloque_obs_tdg_spt_pdf(texto):
    elems = []
    elems.append(Paragraph("OBSERVACIONES TDG-SPT", styles['Heading2']))
    data_obs = [["", Paragraph(texto or "", obs_style)]]
    elems.append(Table(data_obs, colWidths=[120, 400]))
    elems.append(Spacer(1, 4))
    return elems



from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def bloque_power_baterias_pdf(power_dict, cell_style, obs_style, estilo_tabla_basico):
    """
    Genera el bloque POWER - BATERÍAS sin cortes de tabla ni hojas en blanco.
    power_dict: diccionario con los datos.
    cell_style: estilo de celdas normales.
    obs_style: estilo para observaciones (texto largo).
    estilo_tabla_basico: función que retorna un estilo de tabla.
    """
    
    elems = []
    elems.append(Paragraph("POWER - BATERÍAS", styles["Heading2"]))

    # ======== FUNCIÓN AUXILIAR PARA CADA POWER ========
    def tabla_power(n):
        data = [
            [Paragraph(f"POWER {n}", styles["Heading3"]), ""],
            ["Tipo Power", Paragraph(str(power_dict.get(f"Tipo Power {n}", "")), cell_style)],
            ["Marca Power", Paragraph(str(power_dict.get(f"Marca Power {n}", "")), cell_style)],
            ["Tipo de baterías", Paragraph(str(power_dict.get(f"Tipo de baterías {n}", "")), cell_style)],
            ["Cantidad de Bancos de Baterías", Paragraph(str(power_dict.get(f"Cantidad de Bancos de Baterías {n}", "")), cell_style)],
            ["Cantidad de Baterías", Paragraph(str(power_dict.get(f"Cantidad de Baterías {n}", "")), cell_style)],
            ["Estado General de Bancos de Baterías", Paragraph(str(power_dict.get(f"Estado General de Bancos de Baterías {n}", "")), cell_style)],
            ["Cantidad de Rectificadores", Paragraph(str(power_dict.get(f"Cantidad de Rectificadores {n}", "")), cell_style)],
            ["Cantidad de Rectificadores Averiados", Paragraph(str(power_dict.get(f"Cantidad de Rectificadores Averiados {n}", "")), cell_style)],
            ["Corriente de Carga (Amperios DC)", Paragraph(str(power_dict.get(f"Corriente de Carga {n}", "")), cell_style)],
            ["Capacidad de Breaker (Amp)", Paragraph(str(power_dict.get(f"Capacidad de Breaker {n}", "")), cell_style)],
            ["Refrigeración/Ventilación", Paragraph(str(power_dict.get(f"Refrigeración {n}", "")), cell_style)],
            ["Temperatura actual (°C)", Paragraph(str(power_dict.get(f"Temperatura actual {n}", "")), cell_style)],
            ["Autonomía de power (Horas)", Paragraph(str(power_dict.get(f"Autonomía {n}", "")), cell_style)],
            [f"Observaciones Power {n}", Paragraph(str(power_dict.get(f"Observaciones Power {n}", "")), obs_style)],
        ]

        tabla = Table(data, colWidths=[250, 270])
        tabla.setStyle(estilo_tabla_basico())
        return elems

 
    for i in range(1, 4):
        elems.append(tabla_power(i))
        if i < 3:
            elems.append(Spacer(1, 8))

    return elems



def bloque_power_baterias_pdf(power, obs_power=""):
    """
    Genera el bloque POWER - BATERÍAS compatible con la estructura del Streamlit.
    Evita cortes de tabla, hojas en blanco y errores de alineación.
    """

    # ====== ESTILOS ======
    styles = getSampleStyleSheet()
    cell_style = ParagraphStyle(
        name="CellStyle",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        spaceAfter=2
    )
    obs_style = ParagraphStyle(
        name="ObsStyle",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        spaceAfter=4
    )

    def estilo_tabla_basico():
        return [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#121213")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),   # columna de etiquetas
            ("ALIGN", (1, 0), (-1, -1), "LEFT"),  # columna de datos
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica"),
        ]

    elems = [Paragraph("POWER - BATERÍAS", styles["Heading2"])]

    def tabla_power(nombre_power, datos):
        data = [[Paragraph(nombre_power.upper(), styles["Heading3"]), ""]]
        for k, v in datos.items():
            data.append([k, Paragraph(str(v), cell_style)])

        tabla = Table(data, colWidths=[250, 270])
        tabla.setStyle(estilo_tabla_basico())
        return KeepTogether(tabla)

    for nombre_power in ["Power 1", "Power 2", "Power 3"]:
        datos = power.get(nombre_power, {})
        elems.append(tabla_power(nombre_power, datos))
        elems.append(Spacer(1, 8))

    
    if obs_power:
        elems.append(Paragraph("Observaciones Generales Power - Baterías", styles["Heading3"]))
        elems.append(Paragraph(str(obs_power), obs_style))

    return elems


def bloque_planta_electrica_pdf(planta_dict):
    elems = []
    elems.append(Paragraph("PLANTA ELÉCTRICA", styles["Heading2"]))

    # ====== PLANTA 1 ======
    p1 = planta_dict.get("Planta 1", {})
    data1 = [
        [Paragraph("PLANTA 1", styles["Heading3"]), ""],
        ["Horómetro", Paragraph(str(p1.get("Horómetro", "")), cell_style)],
        ["Voltaje de batería de arranque sin cargador", Paragraph(str(p1.get("Voltaje de batería de Arranque sin cargador", "")), cell_style)],
        ["Voltaje de batería de arranque con cargador", Paragraph(str(p1.get("Voltaje de batería de Arranque con cargador", "")), cell_style)],
        ["Nivel de Combustible (%)", Paragraph(str(p1.get("Nivel de Combustible (%)", "")), cell_style)],
        ["Nivel de Refrigerante", Paragraph(str(p1.get("Nivel de Refrigerante", "")), cell_style)],
        ["Nivel de Aceite", Paragraph(str(p1.get("Nivel de Aceite", "")), cell_style)],
        ["Tiene Alarmas Activas", Paragraph(str(p1.get("Tiene Alarmas Activas", "")), cell_style)],
        ["Presenta Fugas de Aceite", Paragraph(str(p1.get("Presenta Fugas de Aceite", "")), cell_style)],
        ["Presenta Fugas de Refrigerante", Paragraph(str(p1.get("Presenta Fugas de Refrigerante", "")), cell_style)],
        ["Estado del Totalizador", Paragraph(str(p1.get("Estado del Totalizador", "")), cell_style)],
        ["Estado de la Tarjeta de Control", Paragraph(str(p1.get("Estado de la Tarjeta de Control", "")), cell_style)],
    ]
    tabla1 = Table(data1, colWidths=[250, 270])
    tabla1.setStyle(estilo_tabla_basico())

    # ====== PLANTA 2 ======
    p2 = planta_dict.get("Planta 2", {})
    data2 = [
        [Paragraph("PLANTA 2", styles["Heading3"]), ""],
        ["Horómetro", Paragraph(str(p2.get("Horómetro", "")), cell_style)],
        ["Voltaje de batería de arranque sin cargador", Paragraph(str(p2.get("Voltaje de batería de Arranque sin cargador", "")), cell_style)],
        ["Voltaje de batería de arranque con cargador", Paragraph(str(p2.get("Voltaje de batería de Arranque con cargador", "")), cell_style)],
        ["Nivel de Combustible (%)", Paragraph(str(p2.get("Nivel de Combustible (%)", "")), cell_style)],
        ["Nivel de Refrigerante", Paragraph(str(p2.get("Nivel de Refrigerante", "")), cell_style)],
        ["Nivel de Aceite", Paragraph(str(p2.get("Nivel de Aceite", "")), cell_style)],
        ["Tiene Alarmas Activas", Paragraph(str(p2.get("Tiene Alarmas Activas", "")), cell_style)],
        ["Presenta Fugas de Aceite", Paragraph(str(p2.get("Presenta Fugas de Aceite", "")), cell_style)],
        ["Presenta Fugas de Refrigerante", Paragraph(str(p2.get("Presenta Fugas de Refrigerante", "")), cell_style)],
        ["Estado del Totalizador", Paragraph(str(p2.get("Estado del Totalizador", "")), cell_style)],
        ["Estado de la Tarjeta de Control", Paragraph(str(p2.get("Estado de la Tarjeta de Control", "")), cell_style)],
    ]
    tabla2 = Table(data2, colWidths=[250, 270])
    tabla2.setStyle(estilo_tabla_basico())

    elems.extend([tabla1, Spacer(1, 14), tabla2])
    return KeepTogether(elems)



def bloque_transferencia_pdf(ats_info):
    elems = []
    elems.append(Paragraph("TRANSFERENCIA (ATS)", styles["Heading2"]))
    data = [["DESCRIPCIÓN", "OBSERVACIÓN"]]

    for k, v in ats_info.items():
        data.append([
            Paragraph(str(k), styles["Normal"]),
            Paragraph(str(v or ""), styles["Normal"])
        ])

    tabla = Table(data, colWidths=[250, 270])
    tabla.setStyle(estilo_tabla_basico())

    elems.append(tabla)
    elems.append(Spacer(1,14))
    return KeepTogether(elems)


def bloque_aires_pdf(aires_data):
    

    elementos = []

    elementos.append(Paragraph("<b>AIRES ACONDICIONADOS</b>", styles["Heading4"]))
    elementos.append(Spacer(1, 6))

    
    for key, valores in aires_data.items():
        if key == "observaciones":
            continue  

        elementos.append(Paragraph(f"<b>{key}</b>", styles["Normal"]))
        data = [["Campo", "Valor"]] + [[k, v] for k, v in valores.items()]
        tabla = Table(data, colWidths=[200, 300])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elementos.append(tabla)
        elementos.append(Spacer(1, 14))

    # Observaciones finales
    if "observaciones" in aires_data and aires_data["observaciones"]:
        elementos.append(Paragraph("<b>Observaciones:</b>", styles["Heading5"]))
        elementos.append(Paragraph(aires_data["observaciones"], styles["Normal"]))

    elementos.append(Spacer(1, 4))
    return elementos





# Estilo de texto pequeño para celdas
cell_style = ParagraphStyle(
    name="cell_style",
    fontSize=6,
    leading=7,
    alignment=1,  
   
)


def bloque_microondas_pdf(microondas_data):
    elems = []
    elems.append(Paragraph("MICROONDAS - INFORMACIÓN GENERAL", styles["Heading2"]))

    radios = [f"RADIO {i}" for i in range(1, 11)]
    col_widths = [130] + [38] * 10

    filas = [
        "Marca de radio MW",
        "Modelo de radio MW",
        "Dirección del enlace",
        "Tiene gestión remota",
        "Potencia de TX (dBm)",
        "Potencia de RX (dBm)",
        "Capacidad de E1’s",
        "Estado de conectores E1’s",
        "Cantidad de puertos Ethernet",
        "Estado de puertos Ethernet",
        "Estado de cable IF",
        "Estado de conectores IF",
        "Marquillas de E1’s y ETH",
        "Marquilla del radio",
        "Se realiza corrección de encintados en ODUs",
        "Radioenlace correctamente aterrizado",
    ]

    # Normalización de claves para coincidencia flexible
    def normalize_key(k):
        if not k:
            return ""
        return (
            k.lower()
            .replace("´", "")
            .replace("’", "")
            .replace("'", "")
            .replace("`", "")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "")
            .replace("°", "")
            .replace("  ", " ")
            .strip()
        )

    # Estilo de texto
    cell_style = ParagraphStyle(
        name="cell_style_microondas",
        fontSize=9,
        leading=10,
        alignment=0,
    )

    data = [["DESCRIPCIÓN"] + radios]

    # Construcción de tabla
    for fila in filas:
        row = [Paragraph(fila, cell_style)]
        fila_norm = normalize_key(fila)

        for i, _ in enumerate(radios):
            valor = ""
            if "Radios" in microondas_data and i < len(microondas_data["Radios"]):
                # Buscar coincidencia flexible entre claves
                radio_dict = microondas_data["Radios"][i]
                for k, v in radio_dict.items():
                    if normalize_key(k) == fila_norm:
                        valor = v
                        break
            row.append(Paragraph(str(valor), cell_style))
        data.append(row)

    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))

    elems.append(tabla)
    elems.append(Spacer(1, 8))

    # Observaciones
    elems.append(Paragraph("OBSERVACIONES MICROONDAS", styles["Heading3"]))
    obs_text = microondas_data.get("Observaciones", "")
    obs_tabla = Table(
        [["Observaciones", Paragraph(obs_text, cell_style)]],
        colWidths=[130, 430]
    )
    obs_tabla.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#97c6e9")),
    ]))
    elems.append(obs_tabla)
    elems.append(Spacer(1, 4))

    return elems





def GSM_850_mhz_pdf(gsm_data):
    elems = [PageBreak(), Paragraph(" INFORMACIÓN GSM 850 MHz", styles["Heading2"]), Spacer(1, 6)]
    data = [["GSM 850 MHz"]]
    for k, v in gsm_data.items():
        data.append([Paragraph(str(k), styles["Normal"]), Paragraph(str(v), styles["Normal"])])
    tabla = Table(data, colWidths=[250, 250])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elems.append(tabla)
    return elems


def bloque_UMTS_850_mhz_pdf(umts_data):
    elems = [PageBreak(), Paragraph(" INFORMACIÓN UMTS 850 MHz", styles["Heading2"]), Spacer(1, 6)]
    data = [["UMTS 850 MHz"]]
    for k, v in umts_data.items():
        data.append([Paragraph(str(k), styles["Normal"]), Paragraph(str(v), styles["Normal"])])
    tabla = Table(data, colWidths=[250, 250])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elems.append(tabla)
    return elems



def bloque_LTE_pdf(lte_data):
    elems = [PageBreak(), Paragraph("INFORMACIÓN LTE", styles["Heading2"]), Spacer(1, 6)]
    data = [["LTE"]]
    for k, v in lte_data.items():
        data.append([Paragraph(str(k), styles["Normal"]), Paragraph(str(v), styles["Normal"])])
    tabla = Table(data, colWidths=[250, 250])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elems.append(tabla)
    return elems


def bloque_S_RAN_pdf(sran_data):
    elems = [PageBreak(), Paragraph(" INFORMACIÓN S-RAN", styles["Heading2"]), Spacer(1, 6)]
    data = [["S-RAN"]]
    for k, v in sran_data.items():
        data.append([Paragraph(str(k), styles["Normal"]), Paragraph(str(v), styles["Normal"])])
    tabla = Table(data, colWidths=[250, 250])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elems.append(tabla)
    return elems




def bloque_AIRSCALE_pdf(airscale_info):
    elems = []

    elems = [PageBreak(), Paragraph(" INFORMACIÓN AIRSCALE", styles["Heading2"]), Spacer(1, 6)]

    airscale_cell_style = ParagraphStyle(
        name="airscale_cell_style",
        fontSize=9,
        leading=10,
        alignment=0,
        wordWrap="CJK",
        spaceBefore=0,
        spaceAfter=0
    )

    header_cell_style = ParagraphStyle(
        name="header_cell_style",
        fontSize=9,
        leading=10,
        alignment=0,
        wordWrap="CJK",
        spaceBefore=0,
        spaceAfter=0,
        fontName="Helvetica"
    )

    
    air_data = airscale_info.get("AIRSCALE", airscale_info)

    data = [
        [Paragraph("AIRSCALE", header_cell_style), Paragraph("", airscale_cell_style)],
        [Paragraph("Banda de Frecuencia", header_cell_style), Paragraph(str(air_data.get("Banda de Frecuencia", "")), airscale_cell_style)],
        [Paragraph("Modelo de System Module´s", header_cell_style), Paragraph(str(air_data.get("Modelo de System Module´s", "")), airscale_cell_style)],
        [Paragraph("Modelo de RF- Module´s", header_cell_style), Paragraph(str(air_data.get("Modelo de RF- Module´s", "")), airscale_cell_style)],
        [Paragraph("Modelo de Targeta de Trasmicion", header_cell_style), Paragraph(str(air_data.get("Modelo de Targeta de Trasmicion", "")), airscale_cell_style)],
        [Paragraph("Version de SW Instalada en System Module", header_cell_style), Paragraph(str(air_data.get("Version de SW Instalada en System Module", "")), airscale_cell_style)],
        [Paragraph("gestion remota de FPFH", header_cell_style), Paragraph(str(air_data.get("gestion remota de FPFH", "")), airscale_cell_style)],
        [Paragraph("Cableado con Amarre Ajustado", header_cell_style), Paragraph(str(air_data.get("Cableado con Amarre Ajustado", "")), airscale_cell_style)],
        [Paragraph("Correccion de Alarmas Precentes", header_cell_style), Paragraph(str(air_data.get("Correccion de Alarmas Precentes", "")), airscale_cell_style)],
        [Paragraph("Estado de Impermeabilizacion de Antenas", header_cell_style), Paragraph(str(air_data.get("Estado de Impermeabilizacion de Antenas", "")), airscale_cell_style)],
        [Paragraph("Jumpers Cableados Correctamente", header_cell_style), Paragraph(str(air_data.get("Jumpers Cableados Correctamente", "")), airscale_cell_style)],
        [Paragraph("Estado de Tierras", header_cell_style), Paragraph(str(air_data.get("Estado de Tierras", "")), airscale_cell_style)],
        [Paragraph("Nro de Antenas por sector", header_cell_style), Paragraph(str(air_data.get("Nro de Antenas por sector", "")), airscale_cell_style)],
        [Paragraph("Capacidad de Breaker de Alimentacion (Amp)", header_cell_style), Paragraph(str(air_data.get("Capacidad de Breaker de Alimentacion (Amp)", "")), airscale_cell_style)],
        [Paragraph("Limpieza de Equipos en piso y en torre(Soplado)", header_cell_style), Paragraph(str(air_data.get("Limpieza de Equipos en piso y en torre(Soplado)", "")), airscale_cell_style)],
        [Paragraph("Limpieza y Aceitado de FAN de Equipos de Acceso en Piso y en Torre", header_cell_style), Paragraph(str(air_data.get("Limpieza y Aceitado de FAN de Equipos de Acceso en Piso y en Torre", "")), airscale_cell_style)],
        [Paragraph("Impermeabilizacion de Puertos de Equipos en Piso", header_cell_style), Paragraph(str(air_data.get("Impermeabilizacion de Puertos de Equipos en Piso", "")), airscale_cell_style)],
        [Paragraph("Impermeabilizacion de Puertos de Equipos en Torre", header_cell_style), Paragraph(str(air_data.get("Impermeabilizacion de Puertos de Equipos en Torre", "")), airscale_cell_style)],
        [Paragraph("Observaciones AIRSCALE", header_cell_style), Paragraph(str(air_data.get("Observaciones AIRSCALE", "")), airscale_cell_style)],
    ]

    col_widths = [220, 280]

    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))

    elems.append(tabla)
    elems.append(Spacer(1, 12))
    return elems




def bloque_alarmas_pdf(alarmas_info):
    elems = [
        Paragraph("ALARMAS", styles["Heading2"]), 
        Spacer(1, 6)
    ]
    data = [["ALARMAS"]]
    headers = [
        "Power en baterías 7401",
        "Falla de rectificador 7402",
        "Falla breaker en baterías 7403",
        "Bajo voltaje de baterías 7404",
        "Alta temperatura en power 7405",
        "Falla fusible de carga 7406",
        "Falla AC power 7407"
    ]

    data = [[Paragraph(h, cell_style) for h in headers]]

    if isinstance(alarmas_info, dict):
        fila = [Paragraph(str(alarmas_info.get(h, "")), cell_style) for h in headers]
        data.append(fila)
    elif isinstance(alarmas_info, list):
        for f in alarmas_info:
            if isinstance(f, dict):
                fila = [Paragraph(str(f.get(h, "")), cell_style) for h in headers]
                data.append(fila)
            else:
                data.append([Paragraph("", cell_style) for _ in headers])
    else:
        data.append([Paragraph("", cell_style) for _ in headers])

    tabla = Table(data, colWidths=[80] * len(headers))
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3c9619")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))

    elems.append(tabla)
    elems.append(Spacer(1, 8))
    return KeepTogether(elems)


def bloque_estados_pdf(estados_info):
    elems = []
    elems.append(Paragraph("ESTADOS DE ALERTA", styles['Heading2']))

    headers = [
        "Planta encendida1 7413",
        "Planta encendida2 7414",
        "Bajo nivel de combustible1 7415",
        "Bajo nivel de combustible2 7416",
        "Falla de AC Comercial 7417",
        "Falla protección sobretensiones 1 7418",
        "Falla protección sobretensiones 2 7419"
    ]
    data = [[Paragraph(h, cell_style) for h in headers]]

    if isinstance(estados_info, dict):
        fila = [Paragraph(str(estados_info.get(h, "")), cell_style) for h in headers]
        data.append(fila)
    elif isinstance(estados_info, list):
        for f in estados_info:
            if isinstance(f, dict):
                fila = [Paragraph(str(f.get(h, "")), cell_style) for h in headers]
                data.append(fila)
            else:
                data.append([Paragraph("", cell_style) for _ in headers])
    else:
        data.append([Paragraph("", cell_style) for _ in headers])

    tabla = Table(data, colWidths=[80] * len(headers))
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0ec2d")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elems.append(tabla)
    elems.append(Spacer(1, 8))
    return KeepTogether(elems)


def bloque_estados_en_rojo_pdf(estados_rojo_info):
    elems = []
    elems.append(Paragraph("ESTADOS CRÍTICOS", styles["Heading2"]))

    headers = [
        "Alta temperatura 7420",
        "Cuarto Puerta abierta 7421"
    ]
    data = [[Paragraph(h, cell_style) for h in headers]]

    if isinstance(estados_rojo_info, dict):
        fila = [Paragraph(str(estados_rojo_info.get(h, "")), cell_style) for h in headers]
        data.append(fila)
    elif isinstance(estados_rojo_info, list):
        for f in estados_rojo_info:
            if isinstance(f, dict):
                fila = [Paragraph(str(f.get(h, "")), cell_style) for h in headers]
                data.append(fila)
            else:
                data.append([Paragraph("", cell_style) for _ in headers])
    else:
        data.append([Paragraph("", cell_style) for _ in headers])

    tabla = Table(data, colWidths=[200, 200])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ad2c2c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elems.append(tabla)
    elems.append(Spacer(1, 8))
    return KeepTogether(elems)



def bloque_ipran_pdf(ipran_data):
    elems = []
    elems.append(Paragraph(" IPRAN", styles["Heading2"]))
    elems.append(Spacer(1, 4))

    equipos = ["Equipo 1", "Equipo 2", "Equipo 3", "Equipo 4", "Equipo 5"]
    col_widths = [130, 75, 75, 75, 75, 75]

    sub_ubicacion = [
        "Rack",
        "Piso",
        "Nombre del Rack (Si Aplica)",
        "Unidad de Rack (Si Aplica)",
        "Fila No. (Si Aplica)"
    ]

    campos_principales = [
        "Referencia equipo Alcatel",
        "ID / Nombre del equipo",
        "Ubicación Física (En caso de NO tener ubicación, dejar descripción breve del equipo)",
        "Temperatura informada por NOC Antes",
        "Temperatura informada por NOC Después",
        "Alarmas tarjeta FAN Crítica (C) - Mayor (MY) - Menor (M)",
        "Inspección visual de FAN en falla (S/N)",
        "Inspección visual patchcord, requieren validación (S/N)",
        "Inspección visual marquillas. Se requiere corrección de marquillas (S/N)",
        "Verificar tarjeta de control (SF/CPM) de qué color se encuentran los indicadores de alarma FAN STATUS (ventiladores) y su operación (aplica para Modelos 7750/7450/7705v2/7250 IXR-e)"
    ]

    cell_style_ipran = ParagraphStyle(name="cell_style_ipran", fontSize=9, leading=10, alignment=0)

    data = [[Paragraph("Campo", cell_style_ipran)] + [Paragraph(eq, cell_style_ipran) for eq in equipos]]

    # Sub-ubicación
    for sub in sub_ubicacion:
        fila = [Paragraph(sub, cell_style_ipran)]
        for i in range(len(equipos)):
            valor = ipran_data["Equipos"][i].get(sub, "") if i < len(ipran_data["Equipos"]) else ""
            fila.append(Paragraph(str(valor or ""), cell_style_ipran))
        data.append(fila)

    # Campos principales
    for campo in campos_principales:
        fila = [Paragraph(campo, cell_style_ipran)]
        for i in range(len(equipos)):
            valor = ipran_data["Equipos"][i].get(campo, "") if i < len(ipran_data["Equipos"]) else ""
            fila.append(Paragraph(str(valor or ""), cell_style_ipran))
        data.append(fila)

    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))

    elems.append(KeepTogether(tabla))
    elems.append(Spacer(1, 8))

    # Observaciones
    elems.append(Paragraph("OBSERVACIONES IPRAN", styles["Heading3"]))
    obs_text = ipran_data.get("Observaciones", "")
    obs_tabla = Table(
        [[Paragraph("Observaciones", cell_style_ipran),
          Paragraph(str(obs_text or ""), cell_style_ipran)]],
        colWidths=[120, 385]
    )
    obs_tabla.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
    ]))
    elems.append(KeepTogether(obs_tabla))
    elems.append(Spacer(1, 8))

    return KeepTogether(elems)


def bloque_transporte_optico(ipran_data):
    elems = []
    elems.append(Paragraph("TRANSPORTE ÓPTICO", styles["Heading2"]))
    elems.append(Spacer(1, 4))

    equipos = ["TX Óptico 1", "TX Óptico 2", "TX Óptico 3", "TX Óptico 4", "TX Óptico 5"]
    col_widths = [130, 75, 75, 75, 75, 75]


    campos_principales = [
        "Referencia equipo transporte óptico",
        "ID / Nombre del equipo",
        "Ubicación Física", "Rack", "Piso",
        "Nombre del Rack (Si Aplica)", "Unidad de Rack (Si Aplica)", "Fila No. (Si Aplica)",
        "Fuente de Voltaje A - PDU (Posición)", "Fuente de Voltaje B - PDU (Posición)",
        "Tiene fuente de respaldo",
        "Temperatura informada por NOC antes", "Temperatura informada por NOC después",
        "Alarmas tarjeta FAN Crítica (C) - Mayor (MY) - Menor (M)",
        "Inspección visual de FAN en falla (S/N)",
        "Inspección visual patchcord ópticos requieren validación (S/N)",
        "Inspección visual marquillas. Se requiere corrección de marquillas (S/N)"
    ]

    cell_style_transporte_optico = ParagraphStyle(
        name="cell_style_transporte_optico",
        fontSize=9,
        leading=10,
        alignment=0  # 0 = izquierda
    )

    data = [[Paragraph("Campo", cell_style_transporte_optico)] + [Paragraph(eq, cell_style_transporte_optico) for eq in equipos]]
    data.append([Paragraph("Ubicación Física (Si aplica)", cell_style_transporte_optico)] + [Paragraph("", cell_style_transporte_optico)] * 5)

    

    for campo in campos_principales:
        fila = [Paragraph(campo, cell_style_transporte_optico)]
        for i in range(len(equipos)):
            valor = ""
            if "Equipos" in ipran_data and i < len(ipran_data["Equipos"]):
                valor = ipran_data["Equipos"][i].get(campo, "")
            fila.append(Paragraph(str(valor or ""), cell_style_transporte_optico))
        data.append(fila)

    # Tabla principal
    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),  # Encabezado azul
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    elems.append(KeepTogether(tabla))
    elems.append(Spacer(1, 8))

    # Bloque de observaciones
    elems.append(Paragraph("OBSERVACIONES IPRAN", styles["Heading3"]))
    obs_text = ipran_data.get("Observaciones", "")
    obs_tabla = Table(
        [[Paragraph("Observaciones", cell_style_transporte_optico),
          Paragraph(str(obs_text or ""), cell_style_transporte_optico)]],
        colWidths=[120, 385]
    )
    obs_tabla.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#97c6e9")),
    ]))
    elems.append(KeepTogether(obs_tabla))
    elems.append(Spacer(1, 8))

    return KeepTogether(elems)





def bloque_observaciones_pdf(texto):
    elems = []
    elems.append(Paragraph("OBSERVACIONES GENERALES", styles['Heading2']))

    
    data_obs = [["Observaciones", Paragraph(texto or "", obs_style)]]
    tabla = Table(data_obs, colWidths=[100, 420])
    tabla.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elems.append(tabla)
    elems.append(Spacer(1, 6))
    return elems



def bloque_infraestructura_pdf(infra_info):
    elems = []
    elems.append(Paragraph(" INFRAESTRUCTURA", styles["Heading2"]))
    elems.append(Spacer(1, 6))

    
    data = [
        ["INFRAESTRUCTURA"],
        ["Estado de las luces de Obstrucción", Paragraph(str(infra_info.get("Estado de las luces de Obstrucción", "")), styles["Normal"])],
        ["Estado del sistema de pararrayos", Paragraph(str(infra_info.get("Estado del sistema de pararrayos", "")), styles["Normal"])],
        ["Estado de la pintura de la torre", Paragraph(str(infra_info.get("Estado de la pintura de la torre", "")), styles["Normal"])],
        ["Estado de la línea de Vida de la torre", Paragraph(str(infra_info.get("Estado de la línea de Vida de la torre", "")), styles["Normal"])],
        ["Extintor Vencido", Paragraph(str(infra_info.get("Extintor Vencido", "")), styles["Normal"])],
        ["Estado de las luces perimetrales", Paragraph(str(infra_info.get("Estado de las luces perimetrales", "")), styles["Normal"])],
        ["Seguridad de la Estación, concertina y muros", Paragraph(str(infra_info.get("Seguridad de la Estación, concertina y muros", "")), styles["Normal"])],
        ["Estado de obra civil", Paragraph(str(infra_info.get("Estado de obra civil", "")), styles["Normal"])],
        ["Poda y Fumigación", Paragraph(str(infra_info.get("Poda y Fumigación", "")), styles["Normal"])],
        ["Estado de puertas de ingreso", Paragraph(str(infra_info.get("Estado de puertas de ingreso", "")), styles["Normal"])],
        ["Observaciones INFRAESTRUCTURA", Paragraph(str(infra_info.get("OBSERVACIONES INFRAESTRUCTURA", "")), styles["Normal"])]
    ]

    
    tabla = Table(data, colWidths=[250, 270])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),  # Encabezado azul
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
    ]))

    elems.append(tabla)
    elems.append(Spacer(1, 8))
    return KeepTogether(elems)





def bloque_observaciones_pdf(texto):
    elems = []
    elems.append(Paragraph("OBSERVACIONES GENERALES", styles['Heading2']))

    
    data_obs = [["Observaciones", Paragraph(texto or "", obs_style)]]
    tabla = Table(data_obs, colWidths=[100, 420])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),   
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),    
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),    
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),   
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),  
        ("TOPPADDING", (0, 0), (-1, -1), 2),        
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2), 
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),  
    ]))
    elems.append(tabla)
    elems.append(Spacer(1, 6))
    
    return elems




def bloque_correctivos_pdf(correctivos_info):
    elems = []
    elems.append(Paragraph(" CORRECTIVOS", styles["Heading2"]))
    elems.append(Spacer(1, 6))  # Menos espacio

   
    header_cell_style = ParagraphStyle(
        name="correctivos_header_style",
        fontSize=9,  # Tamaño más pequeño
        leading=10,   # Espaciado ajustado
        alignment=0,
        wordWrap="CJK",
        spaceBefore=0,
        spaceAfter=0,
        fontName="Helvetica"
    )
    
    content_cell_style = ParagraphStyle(
        name="correctivos_content_style",
        fontSize=9,  # Tamaño más pequeño
        leading=10,   # Espaciado ajustado
        alignment=0,
        wordWrap="CJK",
        spaceBefore=0,
        spaceAfter=0
    )


    data = [
        [Paragraph("CORRECTIVOS A REALIZAR EN LA EB", header_cell_style), Paragraph("", content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO luces de Obstrucción", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO luces de Obstrucción", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO del sistema de pararrayos", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO del sistema de pararrayos", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO de la pintura de la torre", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO de la pintura de la torre", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO de la línea de vida de la torre", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO de la línea de vida de la torre", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO del Extintor", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO del Extintor", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO de las luces perimetrales", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO de las luces perimetrales", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO en la seguridad Estación Base, concertina y muros", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO en la seguridad Estación Base, concertina y muros", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO de obra civil", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO de obra civil", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO poda y/o fumigación", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO poda y/o fumigación", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO de puertas de ingreso", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO de puertas de ingreso", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO equipos de TX", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO equipos de TX", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO Sistemas de Energía", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO Sistemas de Energía", "") or ""), content_cell_style)],
        [Paragraph("Se requiere Reparación/MTO Sistemas de AA", header_cell_style), Paragraph(str(correctivos_info.get("Se requiere Reparación/MTO Sistemas de AA", "") or ""), content_cell_style)],
        [Paragraph("Prioridad General de los Correctivos", header_cell_style), Paragraph(str(correctivos_info.get("PRIORIDAD GENERAL", "") or ""), content_cell_style)],
        [Paragraph("Fecha Estimada para Ejecución de Correctivos", header_cell_style), Paragraph(str(correctivos_info.get("FECHA ESTIMADA EJECUCIÓN", "") or ""), content_cell_style)],
        [Paragraph("Observaciones CORRECTIVOS", header_cell_style), Paragraph(str(correctivos_info.get("OBSERVACIONES CORRECTIVOS", "") or ""), content_cell_style)]
    ]

    
    col_widths = [240, 260]
    
    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#97c6e9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("LEADING", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    
    elems.append(tabla)
    elems.append(Spacer(1, 8))
    
    return elems



def adaptar_datos_microondas(microondas):
    """Convierte el diccionario plano del formulario Streamlit
    en el formato esperado por bloque_microondas_pdf."""
    data = {"Radios": [], "Observaciones": ""}

    # Inicializa 10 radios vacíos
    for _ in range(10):
        data["Radios"].append({})

    for key, value in microondas.items():
        if "Observaciones" in key:
            data["Observaciones"] = value
        else:
            # ejemplo key = "Marca de radio MW_radio3"
            if "_radio" in key:
                nombre, radio = key.rsplit("_radio", 1)
                try:
                    idx = int(radio) - 1
                    if 0 <= idx < 10:
                        data["Radios"][idx][nombre] = value
                except ValueError:
                    pass
    return data


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image as RLImage
from pathlib import Path
import os

styles = getSampleStyleSheet()

# ============================================================
# 🧠 ENCABEZADO (CON IMÁGENES)
# ============================================================
def header_canvas(canvas, doc):
    canvas.saveState()
    width, height = A4

    # 📁 Rutas absolutas (funcionan en local y en Streamlit Cloud)
    base_dir = Path(__file__).parent
    logo_path = base_dir / "logo_claro.png"
    uso_interno_path = base_dir / "uso_interno.png"

    # 🖼️ Logo Claro
    if logo_path.exists():
        try:
            canvas.drawImage(
                str(logo_path),
                50, height - 70,
                width=100,
                height=60,
                preserveAspectRatio=True,
                mask='auto'
            )
        except Exception as e:
            print("⚠️ Error cargando logo:", e)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(30, height - 40, "LOGO CLARO")
    else:
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(30, height - 40, "LOGO CLARO")

    # 🧾 Título central
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(width / 2, height - 40, "FORMATO DE MANTENIMIENTO PREVENTIVO")
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(width / 2, height - 55, "ACCESO")
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(width / 2, height - 70, "OT / Registro")

    # 🧱 Franja "USO INTERNO"
    if uso_interno_path.exists():
        try:
            canvas.drawImage(
                str(uso_interno_path),
                20, height - 100,
                width=width - 30,
                height=30,
                preserveAspectRatio=False,
                mask='auto'
            )
        except Exception as e:
            print("⚠️ Error cargando uso_interno:", e)
            canvas.setFillColorRGB(0.9, 0.9, 0.9)
            canvas.rect(15, height - 100, width - 30, 20, fill=1, stroke=0)
            canvas.setFillColorRGB(0, 0, 0)
            canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(width / 2, height - 95, "USO INTERNO")
    else:
        canvas.setFillColorRGB(0.9, 0.9, 0.9)
        canvas.rect(15, height - 100, width - 30, 20, fill=1, stroke=0)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont("Helvetica", 8)
        canvas.drawCentredString(width / 2, height - 95, "USO INTERNO")

    canvas.restoreState()

# ============================================================
# 📄 GENERACIÓN DEL PDF COMPLETO
# ============================================================
def generar_pdf_completo(datos, output_filename="formato_mantenimiento.pdf"):
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

    # 📋 Documento base
    doc = BaseDocTemplate(
        output_filename,
        pagesize=A4,
        rightMargin=18,
        leftMargin=18,
        topMargin=110,  
        bottomMargin=18
    )

    # 🧱 Marco de contenido
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")

    # 🧩 Plantilla con encabezado
    template = PageTemplate(id="header_template", frames=frame, onPage=header_canvas)
    doc.addPageTemplates([template])

    story = []

    # 🔹 Función auxiliar para agregar bloques al PDF
    def add_block(block):
        if block is None:
            return
        if isinstance(block, list):
            story.extend(block)
        else:
            story.append(block)
        story.append(Spacer(1, 6))

    # 🧱 Secciones del PDF
    add_block(bloque_informacion_general(datos.get("general", {})))
    add_block(bloque_actividades_pdf(datos.get("actividades", {})))
    add_block(bloque_tdg_pdf(datos.get("tdg", {})))
    add_block(bloque_spt_pdf(datos.get("spt", {})))

    obs_tdg_spt = datos.get("obs_tdg_spt", "")
    if obs_tdg_spt:
        add_block(bloque_obs_tdg_spt_pdf(obs_tdg_spt))

    add_block(bloque_power_baterias_pdf(datos.get("power", {})))
    add_block(bloque_planta_electrica_pdf(datos.get("planta", {})))
    add_block(bloque_transferencia_pdf(datos.get("ats", {})))
    add_block(bloque_aires_pdf(datos.get("aires", {})))
    add_block(bloque_microondas_pdf(adaptar_datos_microondas(datos.get("microondas", {}))))
    add_block(GSM_850_mhz_pdf(datos.get("gsm", {})))
    add_block(bloque_UMTS_850_mhz_pdf(datos.get("umts", {})))
    add_block(bloque_LTE_pdf(datos.get("lte", {})))
    add_block(bloque_S_RAN_pdf(datos.get("sran", {})))
    add_block(bloque_AIRSCALE_pdf(datos.get("airscale", {})))
    add_block(bloque_alarmas_pdf(datos.get("alarmas", {})))
    add_block(bloque_estados_pdf(datos.get("estados", {})))
    add_block(bloque_estados_en_rojo_pdf(datos.get("estados_rojo", {})))
    add_block(bloque_ipran_pdf(datos.get("ipran", {})))
    add_block(bloque_transporte_optico(datos.get("transporte_optico", {})))
    add_block(bloque_infraestructura_pdf(datos.get("infraestructura", {})))
    add_block(bloque_correctivos_pdf(datos.get("correctivos", {})))

    # 🔚 Observaciones generales (si existen)
    if "observaciones" in datos:
        add_block(bloque_observaciones_pdf(datos["observaciones"]))

    # 🧾 Generar el documento
    doc.build(story)






# -----------------------
# INTERFAZ STREAMLIT 
# -----------------------

# app.py (copia completa)
import streamlit as st
import base64
import json
from pathlib import Path
from io import BytesIO

# --- ReportLab fallback (solo si no tienes generar_pdf_completo) ---
try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
except Exception:
    # reportlab puede no estar instalado en el entorno; el fallback comprobará eso.
    SimpleDocTemplate = None


# -------------------------
# CONFIG / CARGA IMAGEN
# -------------------------
import os
import base64
from pathlib import Path

# -------------------------
# CONFIG / CARGA IMAGEN
# -------------------------
import base64
from pathlib import Path
import streamlit as st

import streamlit as st
import base64
from pathlib import Path

# -------------------------
# CONFIG / CARGA IMAGEN
# -------------------------
import streamlit as st
import base64
from pathlib import Path

# -------------------------
# CONFIG / CARGA IMAGEN
# -------------------------
from pathlib import Path

BASE_DIR = Path(__file__).parent
IMAGE_PATH = BASE_DIR / "img.png"

def _img_to_base64(path):
    p = Path(path)
    if not p.exists():
        return None
    data = p.read_bytes()
    return base64.b64encode(data).decode()

img_b64 = _img_to_base64(IMAGE_PATH)


# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Formulario Mantenimiento Preventivo", layout="wide")

# -------------------------
# CSS — Banner sin margen superior
# -------------------------
if img_b64:
    banner_css = f"""
    <style>
    /* 🔹 Eliminar el header de Streamlit (icono, título, etc.) */
    header, .stApp header {{
        display: none !important;
    }}

    /* 🔹 Quitar márgenes y padding superiores del contenedor principal */
    .stApp, main .block-container {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}

    /* 🔹 Banner con imagen a pantalla completa superior */
    .banner {{
        position: relative;
        top: 0;
        left: 0;
        width: 100%;
        height: 380px;
        background-image: url("data:image/png;base64,{img_b64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border-bottom: 5px solid #d6001c;
        margin: 0;
        padding: 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }}

    /* 🔹 Contenedor del texto y logo */
    .banner-content {{
        position: relative;
        z-index: 2;
        color: white;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}

    /* 🔹 Logo Claro semitransparente detrás del texto */
    .banner-logo {{
        position: absolute;
        opacity: 0.12;
        width: 80%;
        max-width: 700px;
        filter: brightness(2);
        z-index: 1;
    }}

    /* 🔹 Título principal */
    .banner-title {{
        font-size: 44px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #ffffff;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.6);
        position: relative;
        z-index: 3;
        margin-top: 20px;
    }}

    /* 🔹 Ajuste del contenido para empezar justo debajo del banner */
    main .block-container {{
        padding-top: 10px !important;
    }}
    </style>
    """
else:
    banner_css = """
    <style>
    .banner {
        width: 100%;
        height: 300px;
        background: linear-gradient(90deg,#c70039,#ff5733);
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
        font-size:30px;
        font-weight:700;
        margin:0;
        padding:0;
    }
    </style>
    """

st.markdown(banner_css, unsafe_allow_html=True) 

# -------------------------
# RENDER DEL BANNER
# -------------------------
if img_b64:
    st.markdown(
        """
        <div class="banner">
            <div class="banner-content">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Claro_logo.svg/512px-Claro_logo.svg.png"
                     class="banner-logo">
                <div class="banner-title">FORMULARIO - MANTENIMIENTO PREVENTIVO</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="banner">
            FORMULARIO - MANTENIMIENTO PREVENTIVO
        </div>
        """,
        unsafe_allow_html=True,
    )



# -------------------------
# AUTOCOMPLETE LISTS (editable)
# -------------------------
tipos_baterias = ["AGM", "GEL", "Litio", "Plomo Ácido", "VRLA", "NiMH", "NiCd"]
marcas_power = ["Huawei", "Delta", "Vertiv", "Eaton", "APC", "Eltek", "Siemens"]

# -------------------------
# START FORM (manteniendo TODOS los campos originales)
# -------------------------
# -------- Bloque 1: Información General --------
with st.expander("📝 INFORMACION GENERAL", expanded=True):
    general = {
        "Estación Base": st.text_input("Estación Base", key="g_estacion"),
        "Orden de Trabajo": st.text_input("Orden de Trabajo", key="g_ot"),
        "Fecha de ejecución": st.date_input("Fecha de ejecución", key="g_fecha_ini"),
        "Fecha fin ejecución": st.date_input("Fecha fin ejecución", key="g_fecha_fin"),
        "Personal que ejecutó la actividad": st.text_input("Personal que ejecutó la actividad", key="g_personal"),
        "Descripción breve de ingreso": st.text_area("Descripción breve de ingreso", key="g_desc")
    }


with st.expander("👷‍♂️ ACTIVIDADES", expanded=False):
    actividades = {}
    
    actividades["Limpieza General de EB y Equipos"] = st.selectbox("Limpieza General de EB y Equipos", ["SI", "NO", "NA"], key="act_limp")
    actividades["Descarga de Backups de Equipos de Acceso y Tx"] = st.selectbox("Descarga de Backups", ["SI", "NO", "NA"], key="act_backup")
    actividades["Pruebas de ATS"] = st.selectbox("Pruebas de ATS", ["SI", "NO", "NA"], key="act_ats")
    actividades["Prueba de descarga de baterías"] = st.selectbox("Prueba de descarga de baterías", ["SI", "NO", "NA"], key="act_bat")
    actividades["Certificación de Alarmas"] = st.selectbox("Certificación de Alarmas", ["SI", "NO", "NA"], key="act_alrm")

with st.expander("⚡︎ TDG", expanded=False):
    tdg = {}
    tdg["Capacidad Totalizador principal (Amperios)"] = st.text_input("Capacidad Totalizador principal (Amperios)", key="tdg_cap_princ")
    tdg["Capacidad Totalizador Power 1 (Amperios)"] = st.text_input("Capacidad Totalizador Power 1 (Amperios)", key="tdg_cap_p1")
    tdg["Capacidad Totalizador Power 2 (Amperios)"] = st.text_input("Capacidad Totalizador Power 2 (Amperios)", key="tdg_cap_p2")
    tdg["Capacidad Totalizador Power 3 (Amperios)"] = st.text_input("Capacidad Totalizador Power 3 (Amperios)", key="tdg_cap_p3")
    tdg["Estado General de TDG"] = st.selectbox("Estado General de TDG", ["Bueno", "Regular", "Malo", "NA"], key="tdg_estado")

with st.expander("🧰 SPT", expanded=False):
    spt = {}
    spt["Barraje principal se encuentra instalado"] = st.selectbox("Barraje principal instalado", ["SI", "NO", "NA"], key="spt_barraje")
    spt["Equipos aterrizados adecuadamente"] = st.selectbox("Equipos aterrizados adecuadamente", ["SI", "NO", "NA"], key="spt_aterriz")
    spt["Estado de las Cajas de Paso del SPT"] = st.text_input("Estado de las Cajas de Paso del SPT", key="spt_cajas")

with st.expander("📝 OBSERVACIONES TDG - SPT", expanded=False):
    obs_tdg_spt = st.text_area("Observaciones TDG - SPT", key="obs_tdg_spt")

# -------- Bloque 2: Power (Power 1 / 2 / 3) --------
with st.expander("🔋 POWER - BATERÍAS", expanded=False):
    power = {}

    for i in range(1, 4):
        st.subheader(f"🔋 POWER.{i}")
        power[f"Power {i}"] = {
            "Tipo Power": st.text_input(f"Power {i} - Tipo", key=f"p{i}_tipo"),
            # Autocompletado Marca (selectbox searchable)
            "Marca Power": st.selectbox(
                f"Power {i} - Marca", marcas_power, key=f"p{i}_marca"
            ),
            # Autocompletado Tipo de Baterías (selectbox searchable)
            "Tipo de baterías": st.selectbox(
                f"Power {i} - Tipo de baterías", tipos_baterias, key=f"p{i}_tipo_bat"
            ),
            "Cantidad de Bancos de Baterías": st.number_input(
                f"Power {i} - Cantidad Bancos", min_value=0, key=f"p{i}_bancos"
            ),
            "Cantidad de Baterías": st.number_input(
                f"Power {i} - Cantidad Baterías", min_value=0, key=f"p{i}_baterias"
            ),
            "Estado General de Bancos de Baterías": st.selectbox(
                f"Power {i} - Estado Bancos",
                ["Bueno", "Regular", "Malo", "NA"],
                key=f"p{i}_estado",
            ),
            "Cantidad de Rectificadores": st.number_input(
                f"Power {i} - Rectificadores", min_value=0, key=f"p{i}_rect"
            ),
            "Cantidad de Rectificadores Averiados": st.number_input(
                f"Power {i} - Rectificadores Averiados", min_value=0, key=f"p{i}_rect_av"
            ),
            "Corriente de Carga (Amperios DC)": st.text_input(
                f"Power {i} - Corriente Carga", key=f"p{i}_corr"
            ),
            "Capacidad de Breaker (Amp)": st.text_input(
                f"Power {i} - Breaker", key=f"p{i}_break"
            ),
            "Refrigeración/Ventilación": st.text_input(
                f"Power {i} - Refrigeración", key=f"p{i}_refrig"
            ),
            "Temperatura actual (°C)": st.text_input(
                f"Power {i} - Temperatura", key=f"p{i}_temp"
            ),
            "Autonomía de power (Horas)": st.text_input(
                f"Power {i} - Autonomía", key=f"p{i}_auto"
            ),
        }

with st.expander("📝 OBSERVACIONES POWER", expanded=False):
    obs_power = st.text_area("Observaciones Power - Baterías", key="obs_power")

# -------- Bloque 2: Planta Eléctrica (Planta 1 & Planta 2) --------

# ====================== ⚡ PLANTA ELÉCTRICA ======================
with st.expander("⚡ PLANTA ELÉCTRICA", expanded=False):
    planta = {}

    # Inicializar almacenamiento de historial si no existe
    if "planta_historial" not in st.session_state:
        st.session_state["planta_historial"] = {
            "horometro": [],
            "voltaje_sin": [],
            "voltaje_con": [],
            "combustible": [],
            "refrigerante": [],
            "aceite": [],
            "totalizador": [],
            "tarjeta": [],
        }

    def autocompletar_input(etiqueta, categoria, key):
        """
        Campo de texto con sugerencias dinámicas según lo ya escrito.
        """
        historial = st.session_state["planta_historial"][categoria]
        valor = st.text_input(
            etiqueta,
            key=key,
            placeholder="Escribe o selecciona...",
            value=st.session_state.get(key, ""),
        )

        # Mostrar sugerencias si hay historial y si el texto coincide parcialmente
        if valor:
            sugerencias = [x for x in historial if valor.lower() in x.lower()]
            if sugerencias:
                st.caption("🔎 Sugerencias: " + ", ".join(sugerencias))

        # Guardar nuevo valor si no existe aún
        if valor and valor not in historial:
            historial.append(valor)

        return valor

    # -------------------- PLANTA 1 --------------------
    st.subheader("⚡ PLANTA.1")
    planta["Planta 1"] = {
        "Horómetro": autocompletar_input("Planta 1 - Horómetro", "horometro", "pl1_hor"),
        "Voltaje de batería de Arranque sin cargador": autocompletar_input(
            "Planta 1 - Voltaje sin cargador", "voltaje_sin", "pl1_vs"
        ),
        "Voltaje de batería de Arranque con cargador": autocompletar_input(
            "Planta 1 - Voltaje con cargador", "voltaje_con", "pl1_vc"
        ),
        "Nivel de Combustible (%)": autocompletar_input(
            "Planta 1 - Combustible (%)", "combustible", "pl1_comb"
        ),
        "Nivel de Refrigerante": autocompletar_input(
            "Planta 1 - Refrigerante", "refrigerante", "pl1_ref"
        ),
        "Nivel de Aceite": autocompletar_input(
            "Planta 1 - Aceite", "aceite", "pl1_ace"
        ),
        "Tiene Alarmas Activas": st.selectbox(
            "Planta 1 - Tiene Alarmas Activas", ["SI", "NO", "NA"], key="pl1_alrm"
        ),
        "Presenta Fugas de Aceite": st.selectbox(
            "Planta 1 - Fugas de Aceite", ["SI", "NO", "NA"], key="pl1_fa"
        ),
        "Presenta Fugas de Refrigerante": st.selectbox(
            "Planta 1 - Fugas de Refrigerante", ["SI", "NO", "NA"], key="pl1_fr"
        ),
        "Estado del Totalizador": autocompletar_input(
            "Planta 1 - Estado del Totalizador", "totalizador", "pl1_tot"
        ),
        "Estado de la Tarjeta de Control": autocompletar_input(
            "Planta 1 - Estado Tarjeta Control", "tarjeta", "pl1_tarj"
        ),
    }

    # -------------------- PLANTA 2 --------------------
    st.subheader("⚡ PLANTA.2")
    planta["Planta 2"] = {
        "Horómetro": autocompletar_input("Planta 2 - Horómetro", "horometro", "pl2_hor"),
        "Voltaje de batería de Arranque sin cargador": autocompletar_input(
            "Planta 2 - Voltaje sin cargador", "voltaje_sin", "pl2_vs"
        ),
        "Voltaje de batería de Arranque con cargador": autocompletar_input(
            "Planta 2 - Voltaje con cargador", "voltaje_con", "pl2_vc"
        ),
        "Nivel de Combustible (%)": autocompletar_input(
            "Planta 2 - Combustible (%)", "combustible", "pl2_comb"
        ),
        "Nivel de Refrigerante": autocompletar_input(
            "Planta 2 - Refrigerante", "refrigerante", "pl2_ref"
        ),
        "Nivel de Aceite": autocompletar_input(
            "Planta 2 - Aceite", "aceite", "pl2_ace"
        ),
        "Tiene Alarmas Activas": st.selectbox(
            "Planta 2 - Tiene Alarmas Activas", ["SI", "NO", "NA"], key="pl2_alrm"
        ),
        "Presenta Fugas de Aceite": st.selectbox(
            "Planta 2 - Fugas de Aceite", ["SI", "NO", "NA"], key="pl2_fa"
        ),
        "Presenta Fugas de Refrigerante": st.selectbox(
            "Planta 2 - Fugas de Refrigerante", ["SI", "NO", "NA"], key="pl2_fr"
        ),
        "Estado del Totalizador": autocompletar_input(
            "Planta 2 - Estado del Totalizador", "totalizador", "pl2_tot"
        ),
        "Estado de la Tarjeta de Control": autocompletar_input(
            "Planta 2 - Estado Tarjeta Control", "tarjeta", "pl2_tarj"
        ),
    }



# -------- Bloque 2: ATS (Transferencia) --------
# ====================== 📡 TRANSFERENCIA (ATS) ======================
with st.expander("📡 TRANSFERENCIA (ATS)", expanded=False):
    ats = {}

    # Inicializar historial si no existe
    if "ats_historial" not in st.session_state:
        st.session_state["ats_historial"] = {
            "marca": [],
            "referencia": [],
        }

    def autocompletar_input_ats(etiqueta, categoria, key):
        """
        Campo de texto con memoria y sugerencias dinámicas para ATS
        """
        historial = st.session_state["ats_historial"][categoria]
        valor = st.text_input(
            etiqueta,
            key=key,
            placeholder="Escribe o selecciona...",
            value=st.session_state.get(key, ""),
        )

        # Mostrar sugerencias si hay coincidencias
        if valor:
            sugerencias = [x for x in historial if valor.lower() in x.lower()]
            if sugerencias:
                st.caption("🔎 Sugerencias: " + ", ".join(sugerencias))

        # Guardar nuevo valor si no existe aún
        if valor and valor not in historial:
            historial.append(valor)

        return valor

    # Campos principales
    ats["Marca de la transferencia automática"] = autocompletar_input_ats(
        "Marca de la transferencia automática", "marca", "ats_marca"
    )
    ats["Referencia de la ATS"] = autocompletar_input_ats(
        "Referencia de la ATS", "referencia", "ats_ref"
    )

    ats["Se realiza prueba de encendido de planta (Transferencia y retransferencia)"] = st.selectbox(
        "Se realiza prueba de encendido de planta (Transferencia y retransferencia)",
        ["SI", "NO", "NA"],
        key="ats_prueba",
    )

    ats["Prueba de encendido fue exitosa"] = st.selectbox(
        "Prueba de encendido fue exitosa",
        ["SI", "NO", "NA"],
        key="ats_exitosa",
    )

    ats["Observaciones"] = st.text_area("Observaciones ATS", key="ats_obs")

# -------- Bloque 3: Aires Acondicionados --------
# ====================== 𖣘 AIRES ACONDICIONADOS ======================
with st.expander("𖣘 AIRES ACONDICIONADOS", expanded=False):
    # Inicializa autocompletar
    if "historial_aires_marcas" not in st.session_state:
        st.session_state["historial_aires_marcas"] = []
    if "historial_aires_tipos" not in st.session_state:
        st.session_state["historial_aires_tipos"] = []
    if "historial_aires_capacidades" not in st.session_state:
        st.session_state["historial_aires_capacidades"] = []

    aires = {}

    for i in range(1, 4):
        st.subheader(f"𖣘 AIRES.{i}")
        marca = st.text_input(
            f"Aire {i} - Marca",
            key=f"aire{i}_marca",
            placeholder="Escribe o selecciona una marca anterior",
        )
        tipo = st.text_input(
            f"Aire {i} - Tipo",
            key=f"aire{i}_tipo",
            placeholder="Escribe o selecciona un tipo anterior",
        )
        capacidad = st.text_input(
            f"Aire {i} - Capacidad (BTU)",
            key=f"aire{i}_cap",
            placeholder="Ej: 12000 BTU",
        )
        operativo = st.selectbox(
            f"Aire {i} - Operativo",
            ["SI", "NO"],
            key=f"aire{i}_op"
        )

        # Guarda valores en el diccionario
        aires[f"Aire {i}"] = {
            "Marca": marca,
            "Tipo": tipo,
            "Capacidad (BTU)": capacidad,
            "Operativo": operativo,
        }

        # Actualiza historial si hay nuevo dato
        if marca and marca not in st.session_state["historial_aires_marcas"]:
            st.session_state["historial_aires_marcas"].append(marca)
        if tipo and tipo not in st.session_state["historial_aires_tipos"]:
            st.session_state["historial_aires_tipos"].append(tipo)
        if capacidad and capacidad not in st.session_state["historial_aires_capacidades"]:
            st.session_state["historial_aires_capacidades"].append(capacidad)

    # Observaciones generales
    aires["observaciones"] = st.text_area("Observaciones Aires Acondicionados", key="aires_obs")

# Guarda todo en la sesión
st.session_state["aires"] = aires


# -------- Bloque 3: Microondas (formulario que alimenta la tabla 11x15 en PDF) --------
with st.expander("🛰️ MICROONDAS", expanded=False):
    microondas = {}
    descripciones = [
        "Marca de radio MW",
        "Modelo de radio MW",
        "Dirección del enlace",
        "Tiene gestión remota",
        "Potencia de TX (dBm)",
        "Potencia de RX (dBm)",
        "Capacidad de E1’s",
        "Estado de conectores E1’s",
        "Cantidad de puertos Ethernet",
        "Estado de puertos Ethernet",
        "Estado de cable IF",
        "Estado de conectores IF",
        "Marquillas de E1’s y ETH",
        "Marquilla del radio",
        "Se realiza corrección de encintados en ODUs",
        "Radioenlace correctamente aterrizado",
        "Observaciones Microondas"
    ]

    for desc in descripciones:
        # Convertimos desc a una forma segura para usar en la key
        desc_key = desc.lower().replace(" ", "_").replace("’", "").replace("´", "").replace("(", "").replace(")", "").replace(".", "").replace("°", "")
        
        if desc == "Observaciones Microondas":
            microondas["Observaciones"] = st.text_area("Observaciones Microondas", key=f"micro_obs_{desc_key}")
        else:
            st.markdown(f"**{desc}**")
            cols = st.columns(10)
            for i, col in enumerate(cols, start=1):
                key = f"micro_{desc_key}_radio{i}"
                microondas[f"{desc}_radio{i}"] = col.text_input(f"R{i}", key=key)



# -------- Bloque 3: GSM / UMTS / LTE / SRAN / AirScale --------
with st.expander("🗄️ GSM 850 Mhz"):
    gsm_850 = {}
    st.subheader("🗄️HARDWARE DE GSM")

    fields_order = [
        "Modelo de System Module´s",
        "Modelo de RF- Module´s",
        "Modelo de Targeta de Trasmicion",
        "Version de SW Instalada en System Module",
        "Guia De Onda Ajustada",
        "Cableado con amarres y ajustados",
        "Correccion de Alarmas Precentes",
        "Estado de Impermeabilizacion de Antenas",
        "Jumpers Cableados y Figurados Correctamente",
        "Equipos Aterrizados Correctamente",
        "Nro de Antenas por sector",
        "Capacidad de Breaker de Alimentacion (Amp)",
        "Limpieza de Equipos en piso y en torre(Soplado)",
        "Limpieza y Aceitado de FAN de Equipos de Acceso en Piso y en Torre",
        "Impermeabilizacion de Puertos de Equipos en Piso (Instalacion de capuchones, cubrimiento de orificios, que permiten acceso de humedad y polucion)",
        "Impermeabilizacion de Puertos de Equipos en Torre (Instalacion de capuchones, cubrimiento de orificios, que permiten acceso de humedad y polucion)",
        "Observaciones GSM"
    ]

    for f in fields_order:
        if f == "OBSERVACIONES GSM":
            gsm_850[f] = st.text_area(f, key=f"gsm_obs")
        else:
            gsm_850[f] = st.text_input(f, key=f"gsm_{f}")

with st.expander("🗄️ UMTS 850 Mhz"):
    umts_850 = {}
    st.subheader("Hardware de UMTS")

    fields_order = [
        "Modelo de System Module´s",
        "Modelo de RF- Module´s",
        "Modelo de Targeta de Trasmicion",
        "Version de SW Instalada en System Module",
        "Cableado con amarres y ajustados",
        "Guia De Onda Ajustada",
        "Correccion de Alarmas Precentes",
        "Estado de Impermeabilizacion de Antenas",
        "Jumpers Cableados y Figurados Correctamente",
        "Equipos Aterrizados Correctamente",
        "Nro de Antenas por sector",
        "Capacidad de Breaker de Alimentacion (Amp)",
        "Limpieza de Equipos en piso y en torre(Soplado)",
        "Limpieza y Aceitado de FAN de Equipos de Acceso en Piso y en Torre",
        "Impermeabilizacion de Puertos de Equipos en Piso (Instalacion de capuchones, cubrimiento de orificios, que permiten acceso de humedad y polucion)",
        "Impermeabilizacion de Puertos de Equipos en Torre (Instalacion de capuchones, cubrimiento de orificios, que permiten acceso de humedad y polucion)",
        "Observaciones UMTS"
    ]

    for f in fields_order:
        if f == "OBSERVACIONES UMTS":
            umts_850[f] = st.text_area(f, key=f"umts_obs")
        else:
            umts_850[f] = st.text_input(f, key=f"umts_{f}")

with st.expander("🗄️LTE"):
    lte = {}
    st.subheader("HARDWARE DE LTE")

    fields_order = [
        "Banda de Frecuencia", 
        "Modelo de System Module´s",
        "Modelo de RF- Module´s",
        "Modelo de Targeta de Trasmicion",
        "Modelo de Banda bases",
        "Versión de SW instalada en System Module",
        "Cableado con Amarre Ajustado",
        "Correccion de Alarmas Precentes",
        "Estado de Impermeabilizacion de Antenas",
        "Jumpers Cableados y Figurados Correctamente",
        "Estado de Tierras",
        "Nro de Antenas por sector",
        "Capacidad de Breaker de Alimentacion (Amp)",
        "Limpieza de Equipos en piso y en torre(Soplado)",
        "Limpieza y Aceitado de FAN de Equipos de Acceso en Piso y en Torre",
        "Impermeabilizacion de Puertos de Equipos en Piso (Instalacion de capuchones, cubrimiento de orificios, que permiten acceso de humedad y polucion)",
        "Impermeabilizacion de Puertos de Equipos en Torre (Instalacion de capuchones, cubrimiento de orificios, que permiten acceso de humedad y polucion)",
        "Observaciones LTE"
    ]

    for f in fields_order:
        if f == "📝 OBSERVACIONES LTE":
            lte[f] = st.text_area(f, key=f"LTE_obs")
        else:
            lte[f] = st.text_input(f, key=f"LTE_{f}")

with st.expander("🌐 S_RAN"):
    s_ran = {}
    st.subheader("HARDWARE DE S_RAN")

    fields_order = [
        "Banda de Frecuencia", 
        "Modelo de System Module´s",
        "Modelo de RF- Module´s",
        "Modelo de Targeta de Trasmicion",
        "Modelo de Banda bases",
        "Cableado con Amarre Ajustado",
        "Correccion de Alarmas Precentes",
        "Estado de Impermeabilizacion de Antenas",
        "Jumpers Cableados y Figurados Correctamente",
        "Estado de Tierras",
        "Nro de Antenas por sector",
        "Capacidad de Breaker de Alimentacion (Amp)",
        "Limpieza de Equipos en piso y en torre(Soplado)",
        "Limpieza y Aceitado de FAN de Equipos de Acceso en Piso y en Torre",
        "Impermeabilizacion de Puertos de Equipos en Piso (Instalacion de capuchones, cubrimiento de orificios, que permiten acceso de humedad y polucion)",
        "Impermeabilizacion de Puertos de Equipos en Torre (Instalacion de capuchones, cubrimiento de orificios, que permiten acceso de humedad y polucion)",
        "Observaciones S_RAN"
    ]

    for f in fields_order:
        if f == "📝 OBSERVACIONES S_RAN":
            s_ran[f] = st.text_area(f, key=f"S_RAN_obs")
        else:
            s_ran[f] = st.text_input(f, key=f"S_RAN{f}")

with st.expander("☢ AIRSCALE", expanded=False):
    airscale = {}
    st.subheader("☢ AIRSCALE")

    airscale["AIRSCALE"] = {
        "Banda de Frecuencia": st.text_input("Banda de Frecuencia (AIRSCALE)", key="air_banda"),
        "Modelo de System Module´s": st.text_input("Modelo de System Module´s (AIRSCALE)", key="air_sysmod"),
        "Modelo de RF- Module´s": st.text_input("Modelo de RF- Module´s (AIRSCALE)", key="air_rfmod"),
        "Modelo de Targeta de Trasmicion": st.text_input("Modelo de Targeta de Trasmicion (AIRSCALE)", key="air_tarjeta"),
        "Version de SW Instalada en System Module": st.text_input("Version de SW Instalada (AIRSCALE)", key="air_sw"),
        "gestion remota de FPFH": st.selectbox("Gestión remota de FPFH", ["SI", "NO", "NA"], key="air_fpfh"),
        "Cableado con Amarre Ajustado": st.selectbox("Cableado con Amarre Ajustado", ["SI", "NO", "NA"], key="air_cableado"),
        "Correccion de Alarmas Precentes": st.selectbox("Corrección de Alarmas Presentes", ["SI", "NO", "NA"], key="air_alarmas"),
        "Estado de Impermeabilizacion de Antenas": st.selectbox("Impermeabilización de Antenas", ["Bueno", "Regular", "Malo", "NA"], key="air_imper"),
        "Jumpers Cableados Correctamente": st.selectbox("Jumpers Cableados Correctamente", ["SI", "NO", "NA"], key="air_jumpers"),
        "Estado de Tierras": st.text_input("Estado de Tierras (AIRSCALE)", key="air_tierras"),
        "Nro de Antenas por sector": st.number_input("Nro de Antenas por sector (AIRSCALE)", min_value=0, key="air_antenas"),
        "Capacidad de Breaker de Alimentacion (Amp)": st.text_input("Capacidad de Breaker (AIRSCALE)", key="air_breaker"),
        "Limpieza de Equipos en piso y en torre(Soplado)": st.selectbox("Limpieza de Equipos en piso y torre (AIRSCALE)", ["SI", "NO", "NA"], key="air_limpieza"),
        "Limpieza y Aceitado de FAN de Equipos de Acceso en Piso y en Torre": st.selectbox("Limpieza y Aceitado de FAN (AIRSCALE)", ["SI", "NO", "NA"], key="air_fan"),
        "Impermeabilizacion de Puertos de Equipos en Piso": st.text_area("Impermeabilización de Puertos en Piso (AIRSCALE)", key="air_imp_piso"),
        "Impermeabilizacion de Puertos de Equipos en Torre": st.text_area("Impermeabilización de Puertos en Torre (AIRSCALE)", key="air_imp_torre"),
        "Observaciones AIRSCALE": st.text_area("Observaciones AIRSCALE", key="air_obs")
    }

# Alarmas - Power
with st.expander("🚨 ALARMAS - POWER ", expanded=False):
    st.markdown("🚨Alarmas de Power y baterías**")
    alarmas_info = {}

    cols = st.columns(7)
    etiquetas = [
        "Power en baterías 7401",
        "Falla de rectificador 7402",
        "Falla breaker en baterías 7403",
        "Bajo voltaje de baterías 7404",
        "Alta temperatura en power 7405",
        "Falla fusible de carga 7406",
        "Falla AC power 7407"
    ]

    for i, (col, etiqueta) in enumerate(zip(cols, etiquetas)):
        alarmas_info[etiqueta] = col.selectbox(
            etiqueta,
            ["OK", "Alarmado", "NA"],
            key=f"alarmas_{i}"
        )

with st.expander("📝 Estados Generales", expanded=False):
    st.markdown("**Alarmas de Planta y Combustible**")
    estados_info = {}

    cols = st.columns(7)
    etiquetas = [
        "Planta encendida1 7413",
        "Planta encendida2 7414",
        "Bajo nivel de combustible1 7415",
        "Bajo nivel de combustible2 7416",
        "Falla de AC Comercial 7417",
        "Falla protección sobretensiones 1 7418",
        "Falla protección sobretensiones 2 7419"
    ]

    for i, (col, etiqueta) in enumerate(zip(cols, etiquetas)):
        estados_info[etiqueta] = col.selectbox(
            etiqueta,
            ["OK", "NO", "NA"],
            key=f"estados_{i}"
        )
with st.expander("🚨 Estados Críticos", expanded=False):
    st.markdown("**Alarmas críticas de seguridad**")
    estados_rojo_info = {}

    cols = st.columns(2)
    etiquetas = [
        "Alta temperatura 7420",
        "Cuarto Puerta abierta 7421"
    ]

    for i, (col, etiqueta) in enumerate(zip(cols, etiquetas)):
        estados_rojo_info[etiqueta] = col.selectbox(
            etiqueta,
            ["OK", "NO", "NA"],
            key=f"estados_rojo_{i}"
        )

def bloque_ipran_ui():
    st.subheader("📝 IPRAN")

    ipran_data = {"Equipos": [], "Observaciones": ""}

    equipos = ["Equipo 1", "Equipo 2", "Equipo 3", "Equipo 4", "Equipo 5"]

    campos = [
        "Referencia equipo Alcatel",
        "ID / Nombre del equipo",
        "Ubicación Física (En caso de NO tener ubicación, dejar descripción breve del equipo)",
        "Rack",
        "Piso",
        "Nombre del Rack (Si Aplica)",
        "Unidad de Rack (Si Aplica)",
        "Fila No. (Si Aplica)",
        "Temperatura informada por NOC Antes",
        "Temperatura informada por NOC Después",
        "Alarmas tarjeta FAN Crítica (C) - Mayor (MY) - Menor (M)",
        "Inspección visual de FAN en falla (S/N)",
        "Inspección visual patchcord, requieren validación (S/N)",
        "Inspección visual marquillas. Se requiere corrección de marquillas (S/N)",
        "Verificar tarjeta de control (SF/CPM) de qué color se encuentran los indicadores de alarma FAN STATUS (ventiladores) y su operación (aplica para Modelos 7750/7450/7705v2/7250 IXR-e)"
    ]

    header_cols = st.columns([3, 1, 1, 1, 1, 1])
    header_cols[0].markdown("**Campo**")
    for i, eq in enumerate(equipos):
        header_cols[i + 1].markdown(f"**{eq}**")

    for label in campos:
        cols = st.columns([3, 1, 1, 1, 1, 1])
        cols[0].markdown(f"<b>{label}</b>", unsafe_allow_html=True)
        for i in range(len(equipos)):
            cols[i + 1].text_input(
                "",
                key=f"ipran_{i + 1}_{label}",
                label_visibility="collapsed",
                placeholder=f"{equipos[i]}"
            )

    observaciones = st.text_area("📝 OBSERVACIONES IPRAN (espacio amplio)", key="ipran_observaciones", height=120)

    for i in range(len(equipos)):
        equipo_data = {}
        for label in campos:
            equipo_data[label] = st.session_state.get(f"ipran_{i + 1}_{label}", "")
        ipran_data["Equipos"].append(equipo_data)

    ipran_data["Observaciones"] = observaciones
    return ipran_data


with st.expander("IPRAN", expanded=False):
    ipran = bloque_ipran_ui()

# Transporte Óptico block
def bloque_transporte_optico_ui():
    st.subheader("📝 TRANSPORTE ÓPTICO")

    transp_data = {"Equipos": [], "Observaciones": ""}
    equipos = ["TX Óptico 1", "TX Óptico 2", "TX Óptico 3", "TX Óptico 4", "TX Óptico 5"]

    campos_principales = [
        ("Referencia equipo transporte óptico", "ref_optico"),
        ("ID / Nombre del equipo", "id_equipo"),
        ("Ubicación Física (En caso de NO tener ubicación, dejar descripción breve del equipo)", "ubicacion"),
        ("Rack", "rack"),
        ("Piso", "piso"),
        ("Nombre del Rack (Si Aplica)", "nombre_rack"),
        ("Unidad de Rack (Si Aplica)", "unidad_rack"),
        ("Fila No. (Si Aplica)", "fila_no"),
        ("Fuente de Voltaje A - PDU (Posición)", "voltaje_a"),
        ("Fuente de Voltaje B - PDU (Posición)", "voltaje_b"),
        ("Tiene fuente de respaldo", "respaldo"),
        ("Temperatura informada por NOC antes", "temp_antes"),
        ("Temperatura informada por NOC después", "temp_despues"),
        ("Alarmas tarjeta FAN Crítica (C) - Mayor (MY) - Menor (M)", "alarmas_fan"),
        ("Inspección visual de FAN en falla (S/N)", "insp_fan"),
        ("Inspección visual patchcord ópticos requieren validación (S/N)", "insp_patch"),
        ("Inspección visual marquillas. Se requiere corrección de marquillas (S/N)", "insp_marquillas")
    ]

    # Encabezado tabla
    header_cols = st.columns([3, 1, 1, 1, 1, 1])
    header_cols[0].markdown("**Descripción**")
    for i, eq in enumerate(equipos):
        header_cols[i+1].markdown(f"**{eq}**")

    # Filas
    for label, slug in campos_principales:
        cols = st.columns([3, 1, 1, 1, 1, 1])
        cols[0].markdown(f"<b>{label}</b>", unsafe_allow_html=True)
        for i in range(len(equipos)):
            cols[i+1].text_input(
                "",
                key=f"transp_{slug}_eq{i+1}",  # clave segura y única por módulo
                label_visibility="collapsed",
                placeholder=f"{equipos[i]}"
            )

    # Observaciones (key única)
    observaciones = st.text_area("OBSERVACIONES TRANSPORTE OPTICO", key="transp_observaciones", height=120)

    # Guardar
    for i in range(len(equipos)):
        equipo_data = {}
        for label, slug in campos_principales:
            equipo_data[label] = st.session_state.get(f"transp_{slug}_eq{i+1}", "")
        transp_data["Equipos"].append(equipo_data)

    transp_data["Observaciones"] = observaciones
    return transp_data

with st.expander("17. TRANSPORTE ÓPTICO", expanded=False):
    transporte_optico = bloque_transporte_optico_ui()

# INFRAESTRUCTURA
def bloque_infraestructura_ui():
    st.subheader("🗼 INFRAESTRUCTURA")
    infra = {}
    infra["Estado de las luces de Obstrucción"] = st.text_input("Estado de las luces de Obstrucción", key="infra_luces_obstruccion")
    infra["Estado del sistema de pararrayos"] = st.text_input("Estado del sistema de pararrayos", key="infra_pararrayos")
    infra["Estado de la pintura de la torre"] = st.text_input("Estado de la pintura de la torre", key="infra_pintura_torre")
    infra["Estado de la línea de Vida de la torre"] = st.text_input("Estado de la línea de Vida de la torre", key="infra_linea_vida")
    infra["Extintor Vencido"] = st.selectbox("Extintor Vencido", ["SI", "NO", "NA"], key="infra_extintor")
    infra["Estado de las luces perimetrales"] = st.text_input("Estado de las luces perimetrales", key="infra_luces_perimetrales")
    infra["Seguridad de la Estación, concertina y muros"] = st.selectbox(
        "Seguridad de la Estación, concertina y muros", ["SI", "NO", "NA"], key="infra_seguridad"
    )
    infra["Estado de obra civil"] = st.text_input("Estado de obra civil", key="infra_obra_civil")
    infra["Poda y Fumigación"] = st.selectbox("Poda y Fumigación", ["SI", "NO", "NA"], key="infra_poda")
    infra["Estado de puertas de ingreso"] = st.text_input("Estado de puertas de ingreso", key="infra_puertas")
    infra["OBSERVACIONES INFRAESTRUCTURA"] = st.text_area("OBSERVACIONES INFRAESTRUCTURA", key="infra_observaciones", height=120)
    return infra

with st.expander("🗼INFRAESTRUCTURA", expanded=False):
    infraestructura = bloque_infraestructura_ui()

with st.expander("🔧 CORRECTIVOS", expanded=False):
    st.subheader("🔧 ACTIVIDADES CORRECTIVAS REQUERIDAS")

    correctivos_data = {}

    # Lista de actividades correctivas requeridas
    actividades_correctivas = [
        "Se requiere Reparación/MTO luces de Obstrucción",
        "Se requiere Reparación/MTO del sistema de pararrayos",
        "Se requiere Reparación/MTO de la pintura de la torre",
        "Se requiere Reparación/MTO de la línea de vida de la torre",
        "Se requiere Reparación/MTO del Extintor",
        "Se requiere Reparación/MTO de las luces perimetrales",
        "Se requiere Reparación/MTO en la seguridad Estación Base, concertina y muros",
        "Se requiere Reparación/MTO de obra civil",
        "Se requiere Reparación/MTO poda y/o fumigación",
        "Se requiere Reparación/MTO de puertas de ingreso",
        "Se requiere Reparación/MTO equipos de TX",
        "Se requiere Reparación/MTO Sistemas de Energía",
        "Se requiere Reparación/MTO Sistemas de AA"
    ]

    # 🔹 Mostrar selectboxes para cada actividad
    for actividad in actividades_correctivas:
        clave = actividad.replace("Se requiere Reparación/MTO ", "").replace(" ", "_").upper()
        correctivos_data[actividad] = st.selectbox(
            actividad,
            ["NO REQUERIDO", "REQUERIDO", "EN PROCESO", "COMPLETADO"],
            key=f"correctivo_{clave}"
        )

    # 🔹 Campo de observaciones generales
    correctivos_data["OBSERVACIONES CORRECTIVOS"] = st.text_area(
        "📝 Observaciones Adicionales - Correctivos",
        key="correctivos_observaciones",
        height=120,
        placeholder="Describa aquí cualquier observación adicional sobre las actividades correctivas requeridas..."
    )

    # 🔹 Prioridad general del bloque
    correctivos_data["PRIORIDAD GENERAL"] = st.selectbox(
        "⚙️ Prioridad General de los Correctivos",
        ["BAJA", "MEDIA", "ALTA", "CRÍTICA"],
        key="correctivos_prioridad"
    )

    # 🔹 Fecha estimada de ejecución
    correctivos_data["FECHA ESTIMADA EJECUCIÓN"] = st.date_input(
        "📅 Fecha Estimada para Ejecución de Correctivos",
        key="correctivos_fecha_estimada"
    )

# -----------------------
# Botón: Generar PDF (todo)
# -----------------------
def _generate_simple_pdf_from_dict(datos, output_path):
    """
    Fallback sencillo si no existe la función generar_pdf_completo.
    Crea un PDF con pares clave:valor. Requiere reportlab.
    """
    if SimpleDocTemplate is None:
        raise RuntimeError("ReportLab no está instalado en este entorno; instálalo o provee generar_pdf_completo().")
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("FORMULARIO - MANTENIMIENTO PREVENTIVO", styles["Heading2"]))
    story.append(Spacer(1, 6))
    # Volcamos el dict de forma legible (no demasiado detallado para tablas anidadas)
    for k, v in datos.items():
        story.append(Paragraph(f"<b>{k}</b>", styles["Heading3"]))
        story.append(Spacer(1, 4))
        # si es diccionario anidado, lo convertimos a JSON con indent para legibilidad
        try:
            text = json.dumps(v, ensure_ascii=False, indent=2)
        except Exception:
            text = str(v)
        for line in text.splitlines():
            story.append(Paragraph(line.replace("  ", "&nbsp;&nbsp;"), styles["BodyText"]))
        story.append(Spacer(1, 8))
    doc = SimpleDocTemplate(output_path)
    doc.build(story)

if st.button("📄 Generar PDF Completo"):
    # Ensamblar diccionario de datos con todos los módulos
    datos = {
        "general": general,
        "actividades": actividades,
        "tdg": tdg,
        "spt": spt,
        "obs_tdg_spt": obs_tdg_spt,
        "power": power,
        "obs_power": obs_power,
        "planta": planta,
        "ats": ats,
        "aires": aires,
        "microondas": microondas,
        "gsm": gsm_850,   
        "umts": umts_850,     
        "lte": lte,
        "sran": s_ran,        
        "airscale": airscale,
        "alarmas": alarmas_info,
        "estados": estados_info,
        "estados_rojo": estados_rojo_info,
        "ipran": ipran,  
        "transporte_optico": transporte_optico,
        "infraestructura": infraestructura,
        "correctivos": correctivos_data
    }

    out_file = "formato_mantenimiento.pdf"
    try:
        if "generar_pdf_completo" in globals():
            generar_pdf_completo(datos, output_filename=out_file)
            st.success("✅ PDF completo generado con éxito")
            with open(out_file, "rb") as f:
                st.download_button(
                    "📥 Descargar PDF", 
                    f, 
                    file_name=out_file, 
                    mime="application/pdf"
                )
        else:
            # Fallback: generar JSON como respaldo
            json_str = json.dumps(datos, ensure_ascii=False, indent=2, default=json_serial)
            st.download_button(
                "📥 Descargar datos (JSON) como respaldo",
                json_str,
                file_name="datos_formulario.json",
                mime="application/json"
            )
            st.warning("⚠️ La función 'generar_pdf_completo' no está disponible. Se descargaron los datos en formato JSON.")
    except Exception as e:
        st.error(f"❌ Error al generar PDF: {e}")
        # Intentar generar JSON como último recurso
        try:
            json_str = json.dumps(datos, ensure_ascii=False, indent=2, default=json_serial)
            st.download_button(
                "📥 Descargar datos (JSON) como respaldo",
                json_str,
                file_name="datos_formulario.json",
                mime="application/json"
            )
        except Exception as json_error:
            st.error(f"❌ Error al generar JSON: {json_error}")



