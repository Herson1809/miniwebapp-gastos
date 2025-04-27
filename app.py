import streamlit as st
import pandas as pd

# Configurar página
st.set_page_config(page_title="Análisis de Gastos", page_icon="📊", layout="wide")

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

    # Resumen general con columnas
    st.subheader('📈 Resumen General')
    col1, col2 = st.columns(2)

    with col1:
        total_gastos = df['Monto'].sum()
        st.metric(label="Total de Gastos", value=f"${total_gastos:,.2f}")

    with col2:
        num_sucursales = df['Sucursal'].nunique()
        st.metric(label="Número de Sucursales", value=num_sucursales)

    st.divider()

    # Gastos críticos (mayores a $5,000)
    st.subheader('🚨 Gastos Críticos por Sucursal')
    gastos_criticos = df[df['Monto'] >= 5000]
    gastos_criticos_ordenados = gastos_criticos.sort_values(by=['Sucursal', 'Monto'], ascending=[True, False])

    st.dataframe(gastos_criticos_ordenados, use_container_width=True)

    st.divider()

    # Descargar reporte
    def convertir_excel(df):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    st.download_button(
        label="💾 Descargar Reporte de Gastos Críticos",
        data=convertir_excel(gastos_criticos_ordenados),
        file_name='Reporte_Gastos_Criticos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True
    )
else:
    st.info('📝 Por favor sube un archivo Excel para iniciar.')
