import streamlit as st
import pandas as pd
import plotly.express as px

# --- Pantalla de acceso (contraseña simple editable) ---
def password_gate():
    st.markdown("## 🔒 Acceso restringido")
    
    # CONTRASEÑA ACTUAL --> cámbiala aquí si quieres
    password_correcto = "Daniela300680"  # 🔥 Cambia aquí tu contraseña personal

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
    # --- Resumen de gastos por mes ---
st.subheader('📈 Resumen General por Mes')

# Asegúrate de que la columna 'Fecha' esté en formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  # Convertir la fecha a datetime

# Convertir la fecha a formato "Año-Mes" (Ej: 2025-01, 2025-02)
df['Mes'] = df['Fecha'].dt.strftime('%Y-%m')  # Convertir a formato "Año-Mes"

# Agrupar los datos por mes y calcular el total de cada mes
gastos_por_mes = df.groupby('Mes')['Monto'].sum().reset_index()

# Mostrar los valores de cada mes en columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    enero = gastos_por_mes[gastos_por_mes['Mes'] == '2025-01'].sum()['Monto'] if '2025-01' in gastos_por_mes['Mes'].values else 0
    st.metric(label="Enero", value=f"${enero:,.2f}")

with col2:
    febrero = gastos_por_mes[gastos_por_mes['Mes'] == '2025-02'].sum()['Monto'] if '2025-02' in gastos_por_mes['Mes'].values else 0
    st.metric(label="Febrero", value=f"${febrero:,.2f}")

with col3:
    marzo = gastos_por_mes[gastos_por_mes['Mes'] == '2025-03'].sum()['Monto'] if '2025-03' in gastos_por_mes['Mes'].values else 0
    st.metric(label="Marzo", value=f"${marzo:,.2f}")

with col4:
    abril = gastos_por_mes[gastos_por_mes['Mes'] == '2025-04'].sum()['Monto'] if '2025-04' in gastos_por_mes['Mes'].values else 0
    st.metric(label="Abril", value=f"${abril:,.2f}")

# --- Gráfico de Torta: Distribución de los gastos por categoría ---
st.subheader('🍰 Distribución de Gastos por Categoría')

# Agrupar los datos por categoría y calcular el total de cada una
gastos_por_categoria = df.groupby('Categoria_Limpia')['Monto'].sum().reset_index()

# Crear el gráfico de torta (pastel)
fig_pastel = px.pie(
    gastos_por_categoria,
    names='Categoria_Limpia',
    values='Monto',
    title='Distribución de Gastos por Categoría',
    labels={'Monto': 'Monto Total', 'Categoria_Limpia': 'Categoría'},
    hole=0.3  # Hace que el gráfico tenga el "hueco" central (donut)
)

st.plotly_chart(fig_pastel, use_container_width=True)

    # Agrupar los datos por mes y calcular el total de cada mes
    gastos_por_mes = df.groupby(df['Fecha'].dt.to_period('M'))['Monto'].sum().reset_index()

    # Mostrar los valores de cada mes en columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        enero = gastos_por_

