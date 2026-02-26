# model_utils.py
import os
import base64
from PIL import Image
from openai import OpenAI

# OpenAI Client initialisieren
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_image(img: Image.Image) -> str:
    """
    Klassifiziert ein Bild als 'Pullover', 'Jacke' oder 'Unbekannt' mittels OpenAI.
    
    Parameter:
        img (PIL.Image.Image): Hochgeladenes Bild
    
    Rückgabe:
        str: Kategorie des Bildes
    """

    # Bild in Base64 konvertieren
    import io
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    base64_image = base64.b64encode(img_bytes).decode("utf-8")

    try:
        # Anfrage an OpenAI Chat-Modell mit Bild
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Ist auf diesem Bild eine Jacke oder ein Pullover? "
                                    "Antworte nur mit: Jacke, Pullover oder Unbekannt."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ],
                }
            ],
            max_tokens=10
        )

        # Antwort extrahieren
        result = response.choices[0].message.content.strip()
        if result not in ["Jacke", "Pullover"]:
            return "Unbekannt"
        return result

    except Exception as e:
        print("Fehler bei der Klassifikation:", e)
        return "Unbekannt"

    result = response.choices[0].message.content.strip()
    return result
