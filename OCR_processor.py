import pytesseract
import os
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

input_folder = "image_cleaning_one_folder"
output_file = "extracted_text.txt"


def perform_ocr(input_folder, output_file):
    all_extracted_text = ""

    for filename in os.listdir(input_folder):

        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")
        ):

            image_path = os.path.join(input_folder, filename)

            try:
                image = Image.open(image_path)

                text = pytesseract.image_to_string(image)

                print("-" * 20)
                print(text.strip())
                print("-" * 20)

                all_extracted_text += f"\n--- Text from {filename} ---\n{text}\n"

            except Exception as e:
                print(f"Error in {filename}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_extracted_text)

    print("OCR completed successfully.")


if __name__ == "__main__":
    perform_ocr(input_folder, output_file)