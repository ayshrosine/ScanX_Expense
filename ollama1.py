# from prompt1 import data_conversion
# import subprocess
# import re
# import json

# def get_json_from_prompt(raw_invoice_text:str) -> str:
#     prompt =data_conversion(raw_invoice_text)

#     # 2. Execute Ollama subprocess
#     # Using Llama3 is recommended for better instruction following and JSON formatting.
#     process = subprocess.Popen(
#         ["ollama", "run", "phi3:3.8b"],
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True,
#         encoding='utf-8'
#     )

#     output, error = process.communicate(input=prompt)

#     if process.returncode != 0:
#         raise RuntimeError(f"Ollama failed: {error}")


#     # 3. Clean the LLM output (Crucial for reliable JSON parsing)
#     cleaned_output = output.strip()
    
#     # Use Regex to specifically target and extract content within triple backticks (```json ... ```)
#     # This ensures we get the clean JSON string even if the LLM wraps it.
#     match = re.search(r"```json\n?(.*?)\n?```", cleaned_output, re.DOTALL)
#     if match:
#         json_string = match.group(1).strip()
#     else:
#         # If no markdown block is found, assume the entire output is the JSON
#         # Need to strip out any potential stray ``` or text
#         json_string = cleaned_output.replace("```", "").strip()

#     # 4. converting json string back into dictionary
#     try:
#         return json.loads(json_string)
#     except json.JSONDecodeError as e:
#         print(f"error is {e}")


# if __name__ == "__main__":
#     SAMPLE_INVOICE_TEXT = """
#     Invoice No.: 98765
#     Issue Date: 12/25/2025++
#     Description: Product shipment, Consulting Fee
#     Amount: 500.00, 150.00
#     Grand Total: $650.00
#     """

#     result_dict = get_json_from_prompt(SAMPLE_INVOICE_TEXT)
#     print(result_dict)




from prompt1 import data_conversion
import subprocess
import json
import re

# -------------------------------------------------------
# Model Configuration
# -------------------------------------------------------
MODEL_NAME = "gemma3:4b"


# -------------------------------------------------------
# Call Ollama
# -------------------------------------------------------
def call_ollama(prompt: str) -> str:
    """
    Sends the prompt to Ollama and returns the raw response.
    """

    process = subprocess.Popen(
        ["ollama", "run", MODEL_NAME],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    output, error = process.communicate(input=prompt)

    if process.returncode != 0:
        raise RuntimeError(f"Ollama Error:\n{error}")

    return output.strip()


# -------------------------------------------------------
# Extract JSON
# -------------------------------------------------------
def extract_json(raw_output: str) -> str:
    """
    Extract JSON from markdown if the model returns ```json.
    """

    match = re.search(
        r"```json\s*(.*?)\s*```",
        raw_output,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return raw_output.replace("```", "").strip()


# -------------------------------------------------------
# Repair Invalid JSON
# -------------------------------------------------------
def repair_json(json_string: str) -> str:
    """
    Remove illegal newline characters inside JSON strings.
    """

    repaired = []

    inside_string = False
    escape = False

    for ch in json_string:

        if escape:
            repaired.append(ch)
            escape = False
            continue

        if ch == "\\":
            repaired.append(ch)
            escape = True
            continue

        if ch == '"':
            inside_string = not inside_string
            repaired.append(ch)
            continue

        # Replace illegal newlines inside strings
        if inside_string and ch in ("\n", "\r"):
            repaired.append(" ")
            continue

        repaired.append(ch)

    repaired_json = "".join(repaired)

    # Remove // comments if any
    repaired_json = re.sub(r'//.*', '', repaired_json)

    # Remove /* */ comments if any
    repaired_json = re.sub(
        r'/\*.*?\*/',
        '',
        repaired_json,
        flags=re.DOTALL
    )

    return repaired_json


# -------------------------------------------------------
# Validate JSON
# -------------------------------------------------------
def validate_json(data: dict):

    required_fields = [
        "Invoice_No",
        "Issue_Date",
        "billed_to",
        "billed_by",
        "Description",
        "Amount",
        "Grand_Total"
    ]

    for field in required_fields:

        if field not in data:
            raise ValueError(f"Missing field: {field}")

    # Optional validation only if arrays exist
    if "Description" in data and "Amount" in data:

        if len(data["Description"]) != len(data["Amount"]):
            raise ValueError(
                "Description and Amount lengths do not match."
            )


# -------------------------------------------------------
# Main Function
# -------------------------------------------------------
def get_json_from_prompt(raw_invoice_text: str):

    prompt = data_conversion(raw_invoice_text)

    raw_output = call_ollama(prompt)

    print("=" * 80)
    print("RAW OLLAMA OUTPUT")
    print("=" * 80)
    print(raw_output)
    print("=" * 80)

    json_string = extract_json(raw_output)

    json_string = repair_json(json_string)

    try:

        data = json.loads(json_string)

        validate_json(data)

        return data

    except json.JSONDecodeError as e:

        print("=" * 80)
        print("JSON ERROR")
        print(e)
        print("=" * 80)

        print(json_string)

        return None

    except Exception as e:

        print("=" * 80)
        print("VALIDATION ERROR")
        print(e)
        print("=" * 80)

        return None


# -------------------------------------------------------
# Test
# -------------------------------------------------------
if __name__ == "__main__":

    SAMPLE_INVOICE_TEXT = """
    Invoice No.: 98765
    Issue Date: 12/25/2025
    Description: Product shipment, Consulting Fee
    Amount: 500.00, 150.00
    Grand Total: $650.00
    """

    result = get_json_from_prompt(SAMPLE_INVOICE_TEXT)

    print("\nFINAL RESULT\n")

    print(json.dumps(result, indent=4))