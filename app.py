import streamlit as st
import pandas as pd
import plotly.express as px

# --- Pantalla de acceso (contraseña fija) ---
def password_gate():
    st.markdown("## 🔒 Acceso restringido")
    
    # Aquí está tu clave fija
    password_correcto = "Daniela300680"  # 🔥 Cambié la contraseña a la que me diste

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

    # Convertir la fecha a formato "Año-Mes" (Ej: 2025-01, 2025-02)
    df['Mes'] = df['Fecha'].dt.strftime('%Y-%m')  # Convertir a formato "Año-Mes"

    # Agrupar los datos por mes y calcular el total de cada mes
    gastos_por_mes = df.groupby('Mes')['Monto'].sum().reset_index()

    # Mostrar los valores de cada mes sin color en los recuadros
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        enero = gastos_por_mes[gastos_por_mes['Mes'] == '2025-01']['Monto'].sum() if '2025-01' in gastos_por_mes['Mes'].values else 0
        st.write(f"Enero: ${enero:,.2f}")

    with col2:
        febrero = gastos_por_mes[gastos_por_mes['Mes'] == '2025-02']['Monto'].sum() if '2025-02' in gastos_por_mes['Mes'].values else 0
        st.write(f"Febrero: ${febrero:,.2f}")

    with col3:
        marzo = gastos_por_mes[gastos_por_mes['Mes'] == '2025-03']['Monto'].sum() if '2025-03' in gastos_por_mes['Mes'].values else 0
        st.write(f"Marzo: ${marzo:,.2f}")

    with col4:
        abril = gastos_por_mes[gastos_por_mes['Mes'] == '2025-04']['Monto'].sum() if '2025-04' in gastos_por_mes['Mes'].values else 0
        st.write(f"Abril: ${abril:,.2f}")

    st.divider()

    # --- Gráfico de Barras: Gastos por mes ---
    st.subheader('📊 Gastos por Mes')

    # Crear un gráfico de barras mostrando la evolución de los gastos mes a mes
    fig_barras = px.bar(
        gastos_por_mes,
        x='Mes',
        y='Monto',
        title='Gastos Totales por Mes',
        labels={'Monto': 'Monto Total', 'Mes': 'Mes'},
        color='Monto',
        text_auto=True
    )

    # Corregir la visualización para que se muestren los meses correctamente
    fig_barras.update_layout(
        xaxis_tickmode='array',
        xaxis_tickvals=gastos_por_mes['Mes'],
        xaxis_ticktext=gastos_por_mes['Mes']
    )

    st.plotly_chart(fig_barras, use_container_width=True)

    st.divider()

    # --- Gráfico de Barras: Distribución de los gastos por categoría ---
    st.subheader('🍰 Distribución de Gastos por Categoría')

    # Agrupar los datos por categoría y calcular el total de cada una
    gastos_por_categoria = df.groupby('Categoria_Limpia')['Monto'].sum().reset_index()

    # Crear gráfico de barras en lugar de pastel
    fig_barras_categoria = px.bar(
        gastos_por_categoria,
        x='Categoria_Limpia',
        y='Monto',
        title='Distribución de Gastos por Categoría',
        labels={'Monto': 'Monto Total', 'Categoria_Limpia': 'Categoría'},
        text_auto=True
    )

    st.plotly_chart(fig_barras_categoria, use_container_width=True)

    st.divider()

    # ---
