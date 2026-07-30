# import json

# # Define the precise schema for the extracted invoice data
# JSON_SCHEMA = {
#     "Invoice_No": "The unique invoice identifier.",
#     "Issue_Date": "The date the invoice was created (format: MM/DD/YYYY).",
#     "billed_to": "Name of the company / person to whom bill is charged.",
#     "billed_by": "Name of company who has issued the bill.",
#     "Description": "A list of individual service descriptions",
#     "Amount": "A list of bill amounts for each individual service (must be numbers).Remove all currency symbols like $ or Rs.",
#     "Grand_Total": "The total amount in the bill (must be a single number, float or integer).Remove all currency symbols like $ or Rs."
# }

# def data_conversion(extracted_text:str) -> str:
#     schema_string = json.dumps(JSON_SCHEMA,indent=2)
#     return f"""
# You are an expert in data extraction bot. Your sole task is to analyze the raw data from OCR text from  a single invoice and convert it into a valid JSON object based on the required schema. 

# #Required JSON SCHEMA"
# {schema_string}

# # Extraction Instructions

# - STRICTLY return ONLY one valid JSON object.
# - Do not return markdown.
# - Do not return explanations.
# - Do not return triple backticks.
# - Follow the schema exactly.

# Output Format:

# {
#   "Invoice_No": "",
#   "Issue_Date": "",
#   "billed_to": "",
#   "billed_by": "",
#   "Description": [],
#   "Amount": [],
#   "Grand_Total": 0
# }


# ---
# Raw Invoice text to anlayze:
# {extracted_text}

# IMPORTANT RULES

# 1. Return ONLY valid JSON.
# 2. Do NOT use markdown.
# 3. Do NOT use ```json.
# 4. Do NOT explain anything.
# 5. Every JSON string must be on a single line.
# 6. Never insert a newline inside any string value.
# 7. Amount and Grand_Total must be numbers, not strings.
# 8. Description must be an array of strings.
# 9. Ensure the JSON can be parsed directly using Python's json.loads().

# ---

# """




import json

JSON_SCHEMA = {
    "Invoice_No": "Unique invoice, receipt, order or bill number. Empty string if unavailable.",
    "Issue_Date": "Invoice/Bill date in the original format if possible.",
    "Due_Date": "Due date if present, otherwise empty string.",
    "Purchase_Order": "Purchase order number if available.",
    "billed_to": "Customer, client or company receiving the invoice.",
    "billed_by": "Company, vendor, shop or person issuing the invoice.",
    "Vendor_GST": "Vendor GST/VAT/Tax ID if available.",
    "Customer_GST": "Customer GST/VAT/Tax ID if available.",
    "Currency": "Currency code like INR, USD, EUR etc.",
    "Payment_Method": "Cash, Card, UPI, Credit Card, Bank Transfer etc.",
    "Description": "List of purchased items/services.",
    "Quantity": "List of quantities.",
    "Unit_Price": "List of prices per unit.",
    "Amount": "List of line-item totals.",
    "Subtotal": "Subtotal before taxes.",
    "Discount": "Discount amount.",
    "Tax": "Total tax amount.",
    "Shipping": "Shipping or delivery charge.",
    "Grand_Total": "Final payable amount.",
    "Notes": "Additional notes if present.",
    "source_file": "Leave empty. Python will populate this."
}


def data_conversion(extracted_text: str):

    schema = json.dumps(JSON_SCHEMA, indent=2)

    return f"""
You are an expert Invoice Extraction AI.

Your ONLY responsibility is to convert OCR text into ONE valid JSON object.

The invoice can be from ANY country, ANY language supported by OCR, ANY company, ANY layout and ANY industry.

Never assume a fixed invoice format.

=================================================
EXPECTED JSON SCHEMA
=================================================

{schema}

=================================================
OUTPUT FORMAT
=================================================

{{
    "Invoice_No":"",
    "Issue_Date":"",
    "Due_Date":"",
    "Purchase_Order":"",
    "billed_to":"",
    "billed_by":"",
    "Vendor_GST":"",
    "Customer_GST":"",
    "Currency":"",
    "Payment_Method":"",
    "Description":[],
    "Quantity":[],
    "Unit_Price":[],
    "Amount":[],
    "Subtotal":0,
    "Discount":0,
    "Tax":0,
    "Shipping":0,
    "Grand_Total":0,
    "Notes":"",
    "source_file":""
}}

=================================================
RULES
=================================================

1. Return ONLY one JSON object.

2. Never return markdown.

3. Never return explanations.

4. Never return ```json.

5. Never add text before or after JSON.

6. Never invent information.

7. If a field is missing, return:

Strings → ""

Numbers → 0

Arrays → []

8. OCR may contain broken lines.

Example

Wrong

Apple Juice
500ml Bottle

Correct

Apple Juice 500ml Bottle

9. Merge wrapped text into one sentence.

10. Remove currency symbols.

Example

₹120

becomes

120

$45.20

becomes

45.20

11. Amount, Tax, Discount, Shipping, Subtotal and Grand_Total must be JSON numbers.

12. Description must be an array of strings.

13. Quantity must be an array of numbers.

14. Unit_Price must be an array of numbers.

15. Amount must be an array of numbers.

16. Description, Quantity, Unit_Price and Amount must all have identical lengths.

17. Preserve the order of line items exactly as they appear.

18. Ignore advertisements, logos, QR codes and decorative text.

19. If multiple invoice numbers exist, choose the main invoice/bill number.

20. If multiple totals exist, Grand_Total is the final payable amount.

21. Do not include empty keys that are not defined in the schema.

22. The returned JSON must be valid according to RFC 8259.

=================================================
OCR TEXT
=================================================

{extracted_text}

Return ONLY the JSON.
"""