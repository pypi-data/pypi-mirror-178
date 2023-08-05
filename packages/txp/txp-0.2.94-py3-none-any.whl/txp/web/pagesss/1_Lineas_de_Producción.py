import streamlit as st
import pandas as pd

st.title("Líneas de producción")

st.write(st.session_state.production_lines.to_html(escape=False, index=False), unsafe_allow_html=True)

st.title(
    'Línea rápida de Cereal', 'linea_rapida_cereal'
)

st.title(
    'Linea de empaquetado', 'linea_de_empaquetado'
)
