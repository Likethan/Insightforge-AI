import os
import google.generativeai as genai # type: ignore
import PIL.Image # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

img_path = r"C:\Users\Likethan KJ\.gemini\antigravity\brain\6adbcc5e-e401-4b13-85ac-753e50c0029e\tnra_dashboard_1776359287276.png"
if not os.path.exists(img_path):
    img_path = r"C:\Users\Likethan KJ\.gemini\antigravity\brain\6adbcc5e-e401-4b13-85ac-753e50c0029e\ui_demo.png"

img = PIL.Image.open(img_path)

prompt = "Analyze this Streamlit UI screenshot. List all the exact text, buttons, sliders, checkboxes, select boxes, and sidebar options visible. Detail the layout, including headers, tool options, and any configurations. Provide a comprehensive breakdown of the 'options used' and 'tools used' shown in the interface so I can recreate it exactly in Streamlit code."

try:
    response = model.generate_content([prompt, img])
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print("=== UI DESCRIPTION ===")
    print(response.text)
    
    # Save the output directly to a file to avoid PowerShell redirection encoding issues
    output_path = "ui_description.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"\nSaved description to: {output_path}")
except Exception as e:
    print(f"ERROR: {e}")
