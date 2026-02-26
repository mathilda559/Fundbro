# app.py
import streamlit as st
from PIL import Image
import os
import pandas as pd
import uuid
from model_utils import classify_image

# Streamlit-Seite konfigurieren
st.set_page_config(page_title="Schul-Fundbüro", layout="wide")
st.title("🧥 Schul Online-Fundbüro")

# Upload-Ordner sicherstellen
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# CSV-Datenbank
DB_FILE = "database.csv"
def save_entry(title, category, image_path):
    new_entry = pd.DataFrame([{
        "Titel": title,
        "Kategorie": category,
        "Bild": image_path
    }])
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry
    df.to_csv(DB_FILE, index=False)

def load_entries():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Titel", "Kategorie", "Bild"])

# --- Upload-Bereich ---
st.header("📤 Neues Fundstück hochladen")
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png", "jpeg"])
title = st.text_input("Titel des Fundstücks")

if uploaded_file and title:
    img = Image.open(uploaded_file)

    # KI-Klassifikation (robust)
    category = classify_image(img)

    # Eindeutiger Bildname
    unique_name = str(uuid.uuid4()) + ".jpg"
    image_path = os.path.join(UPLOAD_FOLDER, unique_name)
    img.save(image_path)

    # Daten speichern
    save_entry(title, category, image_path)
    st.success(f"Gespeichert als {category}")

# --- Galerie ---
st.header("📚 Gefundene Gegenstände")
entries = load_entries()

if not entries.empty:
    cols = st.columns(3)
    for idx, row in entries.iterrows():
        with cols[idx % 3]:
            st.image(row["Bild"], use_column_width=True)
            st.markdown(f"**{row['Titel']}**")
            st.write(f"Kategorie: {row['Kategorie']}")
else:
    st.info("Noch keine Fundstücke hochgeladen.")
