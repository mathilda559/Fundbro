import streamlit as st
from PIL import Image
import os
from model_utils import classify_image
from database import save_entry, load_entries

st.set_page_config(page_title="Schul-Fundbüro", layout="wide")

st.title("🧥 Schul Online-Fundbüro")

if not os.path.exists("uploads"):
    os.makedirs("uploads")

st.header("📤 Neues Fundstück hochladen")

uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png", "jpeg"])
title = st.text_input("Titel des Fundstücks")

if uploaded_file and title:
    img = Image.open(uploaded_file)

    category = classify_image(img)

    image_path = os.path.join("uploads", uploaded_file.name)
    img.save(image_path)

    save_entry(title, category, image_path)

    st.success(f"Gespeichert als {category}")

st.header("📚 Gefundene Gegenstände")

entries = load_entries()

cols = st.columns(3)

for index, row in entries.iterrows():
    with cols[index % 3]:
        st.image(row["Bild"], use_column_width=True)
        st.markdown(f"**{row['Titel']}**")
        st.write(f"Kategorie: {row['Kategorie']}")
