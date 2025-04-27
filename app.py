import streamlit as st
import pandas as pd

# --- Pantalla de acceso (contraseña simple editable) ---
def password_gate():
    st.markdown("## 🔒 Acceso restringido")
    
    # CONTRASEÑA ACTUAL --> cámbiala aquí por la que tú quieras
    password_correcto = "MiClave123"  # 🔥 Cambia "MiClave123" por tu nueva contraseña

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
st.set_page_config(page_title="An_

                   
