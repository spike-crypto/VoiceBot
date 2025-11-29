"""
Extract resume text from PDF and save as JSON
"""
import pathlib
import sys
import json
import re
from pdfminer.high_level import extract_text

# Get the PDF path
pdf_path = pathlib.Path(__file__).parent / "Balamurugan_AI_Engg (2).pdf"

if not pdf_path.is_file():
    print(f"❌ PDF not found at {pdf_path}")
    sys.exit(1)

print(f"📄 Extracting text from {pdf_path.name}...")

# Extract text
text = extract_text(str(pdf_path))

# Clean up the text - collapse multiple newlines
clean = re.sub(r"\n{3,}", "\n\n", text.strip())

# Save to JSON
out_path = pathlib.Path(__file__).parent / "frontend" / "src" / "resume_text.json"
out_path.parent.mkdir(parents=True, exist_ok=True)

with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"resume": clean}, f, ensure_ascii=False, indent=2)

print(f"✅ Résumé extracted to {out_path}")
print(f"📊 Total characters: {len(clean)}")
