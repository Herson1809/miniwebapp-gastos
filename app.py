import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Clave fija
clave = "Daniela300680"

# Función para verificar la clave
def verificar_clave():
    clave_ingresada = st.text_input("Introduce la clave para continuar", type="password")
    if clave_ingresada != clave:
        st.error("¡Clave incorrecta! No tienes acceso.")
        return False
    return True

# Verificar clave antes de mostrar la aplicación
if not verificar_clave():
    st.stop()

# Título de la aplicación
st.title("Mini WebApp de Gastos - Herson Stan")

# Cargar archivo
uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx"])
if uploaded_file is not None:
    # Cargar datos de Excel
    df = pd.read_excel(uploaded_file, sheet_name='Hoja1')  # Ajusta 'Hoja1' según tu archivo

    # Mostrar datos cargados
    if st.checkbox('Mostrar datos cargados'):
        st.write(df)

    # Resumen general por mes
    st.subheader("Resumen General por Mes")
    resumen_mes = df.groupby(df['Fecha'].dt.to_period('M'))['Monto'].sum().reset_index()
    for index, row in resumen_mes.iterrows():
        st.write(f"{row['Fecha']}: ${row['Monto']:,.2f}")

    # Gastos por mes
    st.subheader("Gastos por Mes")
    df['Mes'] = df['Fecha'].dt.month
    gastos_mes = df.groupby('Mes')['Monto'].sum()
    st.write(gastos_mes)

    # Gráfica de gastos por mes
    st.subheader("Gráfico de Gastos por Mes")
    fig, ax = plt.subplots()
    ax.bar(gastos_mes.index, gastos_mes.values)
    ax.set_xlabel('Mes')
    ax.set_ylabel('Monto Total')
    ax.set_title('Gastos Totales por Mes')
    st.pyplot(fig)

    # Semáforo de alertas (ficticio, ejemplo)
    st.subheader("Semáforo de Alertas")
    umbral_gasto = 500000000  # Umbral de gasto
    if resumen_mes['Monto'].iloc[-1] > umbral_gasto:
        st.markdown('<p style="color:red;">🚨 ¡ALERTA! El gasto del último mes supera el umbral 🚨</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:green;">✅ El gasto está dentro del rango seguro ✅</p>', unsafe_allow_html=True)

    # Lista de los gastos críticos
    st.subheader("Gastos Críticos a Revisar")
    umbral_critico = 10000000  # Umbral para considerar un gasto como crítico
    gastos_criticos = df[df['Monto'] > umbral_critico]
    gastos_criticos_lista = gastos_criticos[['Fecha', 'Categoria_Limpia', 'Monto']]
    
    if not gastos_criticos_lista.empty:
        st.write(gastos_criticos_lista)
    else:
        st.write("No hay gastos críticos por encima del umbral.")
