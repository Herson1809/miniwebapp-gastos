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
if not password_gate_
