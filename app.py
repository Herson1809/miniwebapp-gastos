import streamlit as st
import pandas as pd
import plotly.express as px

# --- Pantalla de acceso (contraseña simple editable) ---
def password_gate():
    st.markdown("## 🔒 Acceso restringido")
    
    # CONTRASEÑA ACTUAL --> cámbiala aquí si quieres
    password_correcto = "MiClave123"  # 🔥 Cambia aquí tu contraseña personal

    password = st.text_input("Ingrese la contraseña:", type="password")
    
    if password == password_correcto:
        st.success("Acceso concedido ✅")
        return True
    elif password == "":
        return False
    else:
        st.error("Contraseña incorrecta ❌")
        return False

# Configurar página
st.set_page_config(page_title="Análisis de Gastos", page_icon="📊", layout="wide")

# Verificar acceso antes de mostrar la app
if not password_gate():
    st.stop()

# Encabezado principal elegante
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>📊 Mini WebApp de Gastos</h1>
    <h3 style='text-align: center;'>Análisis Automático de Gastos por Sucursal</h3>
""", unsafe_allow_html=True)

st.divider()

# Subir archivo Excel
uploaded_file = st.file_uploader("**Sube tu archivo Excel de Gastos**", type=["xlsx"])

if uploaded_file is not None:
    # Leer el Excel
    df = pd.read_excel(uploaded_file)

    st.success('✅ Archivo cargado exitosamente')

    # Mostrar datos cargados
    if st.checkbox('📄 Mostrar datos cargados'):
        st.dataframe(df, use_container_width=True)

    st.divider()

    # --- Resumen de gastos por mes ---
    st.subheader('📈 Resumen General por Mes')

    # Asegúrate de que la columna 'Fecha' esté en formato datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  # Convertir la fecha a datetime

    # Agrupar los datos por mes y calcular el total de cada mes
    gastos_por_mes = df.groupby(df['Fecha'].dt.to_period('M'))['Monto'].sum().reset_index()

    # Mostrar los valores de cada mes en columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        enero = gastos_por_

