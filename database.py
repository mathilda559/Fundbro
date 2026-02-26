import pandas as pd
import os

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
