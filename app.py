import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para controlar el acceso con una clave
def acceso_restringido():
    password = st.text_input("Ingrese la contraseña:", type="password")
    if password == "tu_clave_secreta":  # Cambia esto a tu clave
        st.success("Acceso concedido")
        return True
    elif password:
        st.error("Contraseña incorrecta")
        return False
    return False

# Si el acceso es concedido, se permite cargar los datos
if acceso_restringido():
    st.title("Mini webApp de Gastos - Herson Stan")

    # Cargar archivo Excel
    uploaded_file = st.file_uploader("Cargar archivo de gastos en formato Excel", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        # Mostrar los primeros datos cargados
        st.write("Datos cargados:")
        st.write(df.head())

        # Mostrar resumen de gastos por mes
        st.subheader("Resumen General por Mes")
        resumen_mes = df.groupby('MES')['Monto'].sum()
        st.write(resumen_mes)

        # Crear un gráfico para el resumen de gastos
        st.subheader("Gráfico de Gastos por Mes")
        fig, ax = plt.subplots()
        resumen_mes.plot(kind="bar", ax=ax)
        ax.set_xlabel("Mes")
        ax.set_ylabel("Monto")
        ax.set_title("Gastos por Mes")
        st.pyplot(fig)

        # Mostrar lista de los 10 gastos más críticos (por ejemplo, los más altos)
        st.subheader("Los 10 Gastos Más Críticos")
        top_gastos = df.nlargest(10, 'Monto')
        st.write(top_gastos[['Categoria_Limpia', 'Monto']])

        # También puedes mostrar un gráfico de estos 10 gastos
        st.subheader("Gráfico de los 10 Gastos Más Críticos")
        fig2, ax2 = plt.subplots()
        top_gastos.plot(kind="bar", x="Categoria_Limpia", y="Monto", ax=ax2)
        ax2.set_xlabel("Categoría")
        ax2.set_ylabel("Monto")
        ax2.set_title("Top 10 Gastos Críticos")
        st.pyplot(fig2)

    else:
        st.info("Por favor, cargue un archivo para comenzar.")
