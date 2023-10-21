import streamlit as st
import pandas as pd
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image


title = 'Predict the painter from a Paint' 
description = """ ═════════════════════════

<u>**GOAL OF THIS PROJECT**</u> : 

- The goal of the project is to **the author of the painting** from the image of the paint itself. 
- Fine Tuning training of an existing model architecture(**MobilenetV3-S**) 
but with high efficiency (**ROC 0.98**) 
- further optimized through **quantization of the dynamic range**. 
- Original model in .h5 format was **4.5MB**, the quantized .tfllite one 
becomes **1.1MB**, loaded with tflite-runtime, useful for **low-performance** systems with **small storage**.
"""
image = 'stlib/files/Art.png'
def run():
    st.header(title)
    # Carica il file CSV
    @st.cache_data  # Cache per migliorare le prestazioni
    def load_data():
        data = pd.read_csv('stlib/files/painter.csv')
        data = data.sort_values(by="Painter", ascending=True)
        data = data.reset_index(drop=True)
        return data

    data = load_data()
    
    # Crea due colonne
    col1, col2 = st.columns([1,3])

    # Colonna 1: Mostra la lista Markdown
    with col1:
        st.dataframe(data,use_container_width=True, height=800)

    # Colonna 2: Pulsante per l'upload di un file immagine
    
    with col2:
            st.markdown(" **Add your file here** :")
            uploaded_file = st.file_uploader("**LOAD IMAGE**", type=["jpg", "png"])
            result = st.empty()
            # Puoi utilizzare uploaded_file per processare l'immagine caricata
            if uploaded_file is not None:
                # Esempio: visualizza l'immagine caricata
                st.image(uploaded_file, use_column_width=True)

                # Carica il modello TF Lite
                interpreter = tflite.Interpreter(model_path='stlib/files/painter.tflite')

                # Alloca i tensori del modello
                interpreter.allocate_tensors()

                # Ottieni i dettagli dei tensori di input e output
                input_details = interpreter.get_input_details()
                output_details = interpreter.get_output_details()

                # Leggi l'immagine uploaded_file usando PIL
                image = Image.open(uploaded_file)

                # Ridimensiona l'immagine secondo la forma del tensore di input
                input_shape = input_details[0]['shape']
                image = image.resize((input_shape[1], input_shape[2]))

                # Converte l'immagine in un array numpy
                image = np.array(image)

                # Aggiungi una dimensione batch se necessario
                if len(input_shape) == 4:
                    image = np.expand_dims(image, axis=0)

                # Imposta il tensore di input del modello con il valore dell'immagine
                image = np.float32(image)
                interpreter.set_tensor(input_details[0]['index'], image)

                # Invoca il modello
                interpreter.invoke()

                # Ottieni il valore del tensore di output del modello
                output_data = interpreter.get_tensor(output_details[0]['index'])

                # Interpreta i dati di output in base al tipo di modello. Per esempio, se il modello è una classificazione di pittori, puoi usare il seguente codice per ottenere il pittore più probabile:

                # Crea una lista dei possibili pittori
                painters = data.values

                # Ottieni l'indice del pittore con la probabilità più alta
                painter_index = np.argmax(output_data)

                # Stampa il pittore e la probabilità
                result.markdown(f" ### Painter: {painters[painter_index][0]}, &emsp; &emsp; &emsp; Probability: {output_data[0][painter_index]}")
    if __name__ == "__main__":
        run()
