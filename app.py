import streamlit as st
import pandas as pd

# --- Pantalla de acceso (contraseña simple) ---
def password_gate():
    st.markdown("## 🔒 Acceso restringido")
    password = st.text_input("Ingrese la contraseña:", type="password")
    if password == "MiClave123":  # <-- Cambia aquí tu contraseña personal
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

    # Resumen general
    st.subheader('📈 Resumen General')
    col1, col2 = st.columns(2)

    with col1:
        total_gastos = df['Monto'].sum()
        st.metric(label="Total de Gastos", value=f"${total_gastos:,.2f}")

    with col2:
        num_sucursales =_

