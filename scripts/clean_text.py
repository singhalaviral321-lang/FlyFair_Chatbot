import re

INPUT_PATH = "/Users/aviralsinghal/Documents/FlyFair_data/extracted_text/full_raw.txt"
OUTPUT_PATH = "/Users/aviralsinghal/Documents/FlyFair_data/cleaned_text/clean.txt"

with open(INPUT_PATH, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Normalize excessive newlines
text = re.sub(r'\n{3,}', '\n\n', text)

# Fix common OCR issues
text = text.replace('ﬂ', 'fl')
text = text.replace('₹', 'Rs ')
text = text.replace('–', '-')
text = text.replace('—', '-')

# Strip trailing whitespace
text = text.strip()

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("✅ Cleaned text written to cleaned_text/clean.txt")
