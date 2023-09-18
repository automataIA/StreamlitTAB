import streamlit as st
from PIL import Image

title = """Choose Projects here..."""
description = """ """
image = 'stlib/files/home.png'
st.cache
def run():
    st.markdown("# \n\n")
    
    co = st.columns(5)

    with co[2]:
        st.image(image)
        # Imposta l'immagine come sfondo della pagina
    
    titolo = 'Data Scientist'
    st.markdown("<h1 style='text-align: center; padding: 1px; height: 200px;'>"+str(titolo)+"</h1>", unsafe_allow_html=True)

        

if __name__ == "__main__":
     run()