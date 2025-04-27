import streamlit as st
import pandas as pd

# Título principal
st.title('Mini WebApp de Gastos')
st.subheader('Análisis Automático de Gastos por Sucursal')

# Subir archivo Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel de Gastos", type=["xlsx"])

if uploaded_file is not None:
    # Leer el Excel
    df = pd.read_excel(uploaded_file)

    st.success('Archivo cargado exitosamente ✅')

    # Mostrar datos cargados
    if st.checkbox('Mostrar datos cargados'):
        st.dataframe(df)

    # Resumen general
    st.header('Resumen General 📊')
    total_gastos = df['Monto'].sum()
    num_sucursales = df['Sucursal'].nunique()

    st.metric(label="Total de Gastos", value=f"${total_gastos:,.2f}")
    st.metric(label="Número de Sucursales", value=num_sucursales)

    # Gastos críticos (mayores a $5,000)
    st.header('Gastos Críticos por Sucursal 🚨')
    gastos_criticos = df[df['Monto'] >= 5000]
    gastos_criticos_ordenados = gastos_criticos.sort_values(by=['Sucursal', 'Monto'], ascending=[True, False])

    st.dataframe(gastos_criticos_ordenados)

    # Descargar reporte
    def convertir_excel(df):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    st.download_button(
        label="Descargar Reporte de Gastos Críticos",
        data=convertir_excel(gastos_criticos_ordenados),
        file_name='Reporte_Gastos_Criticos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    st.info('Por favor sube un archivo Excel para iniciar.')

