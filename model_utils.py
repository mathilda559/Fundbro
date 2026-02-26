import os
import base64
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_image(img: Image.Image) -> str:
    import io
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    base64_image = base64.b64encode(img_bytes).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Schau dir dieses Bild an und bestimme nur die Kategorie:\n"
                                "Jacke oder Pullover?\n"
                                "Antworte nur mit einem Wort: 'Jacke' oder 'Pullover'."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            max_tokens=10
        )

        result = response.choices[0].message.content.strip().lower()
        if "jacke" in result or "coat" in result:
            return "Jacke"
        elif "pullover" in result or "sweater" in result:
            return "Pullover"
        else:
            return "Unbekannt"

    except Exception as e:
        print("Fehler bei der Klassifikation:", e)
        return "Unbekannt"
