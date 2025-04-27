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

    # Resumen general
    st.subheader('📈 Resumen General')
    col1, col2 = st.columns(2)

    with col1:
        total_gastos = df['Monto'].sum()
        st.metric(label="Total de Gastos", value=f"${total_gastos:,.2f}")

    with col2:
        num_sucursales = df['Sucursal'].nunique()
        st.metric(label="Número de Sucursales", value=num_sucursales)

    st.divider()

    # Sección de filtros
    st.subheader('🛠️ Filtros de Análisis')

    sucursales_disponibles = df['Sucursal'].dropna().unique().tolist()
    sucursales_disponibles = sorted(sucursales_disponibles)

    sucursal_seleccionada = st.selectbox('Selecciona una Sucursal:', options=['Todas'] + sucursales_disponibles)
    monto_minimo = st.number_input('Monto mínimo para mostrar', min_value=0, value=5000, step=500)

    if sucursal_seleccionada != 'Todas':
        df_filtrado = df[(df['Sucursal'] == sucursal_seleccionada) & (df['Monto'] >= monto_minimo)]
    else:
        df_filtrado = df[df['Monto'] >= monto_minimo]

    st.divider()

    # Mostrar Gastos Críticos filtrados
    st.subheader('🚨 Gastos Críticos Filtrados')
    gastos_criticos_ordenados = df_filtrado.sort_values(by=['Sucursal', 'Monto'], ascending=[True, False])

    st.dataframe(gastos_criticos_ordenados, use_container_width=True)

    st.divider()

    # Gráfico de Barras: Top 10 Sucursales
    st.subheader('📊 Top 10 Sucursales por Monto de Gastos')

    top_sucursales = df_filtrado.groupby('Sucursal')['Monto'].sum().sort_values(ascending=False).head(10).reset_index()

    fig = px.bar(
        top_sucursales,
        x='Sucursal',
        y='Monto',
        title='Top 10 Sucursales con Mayor Monto de Gastos',
        labels={'Monto': 'Monto Total', 'Sucursal': 'Sucursal'},
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- Sección de Auditoría Automática ---
    st.subheader('🛡️ Auditoría de Gastos Sospechosos')

    # Función para asignar colores de semáforo
    def asignar_semaforo(monto):
        if monto > 50000:
            return '🟥 Crítico'
        elif monto > 20000:
            return '🟨 Moderado'
        else:
            return '🟩 Bajo'

    df_auditoria = df_filtrado.copy()
    df_auditoria['Riesgo'] = df_auditoria['Monto'].apply(asignar_semaforo)

    df_sospechosos = df_auditoria[df_auditoria['Riesgo'] != '🟩 Bajo']

    if not df_sospechosos.empty:
        st.warning(f"🚨 Se detectaron {len(df_sospechosos)} transacciones sospechosas:")
        st.dataframe(df_sospechosos[['Sucursal', 'Monto', 'Riesgo']], use_container_width=True)
    else:
        st.success("✅ No se detectaron transacciones sospechosas.")

    st.divider()

    # Descargar reporte filtrado
    def convertir_excel(df):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    st.download_button(
        label="💾 Descargar Reporte Filtrado",
        data=convertir_excel(gastos_criticos_ordenados),
        file_name='Reporte_Gastos_Filtrado.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True
    )

else:
    st.info('📝 Por favor sube un archivo Excel para iniciar.')
