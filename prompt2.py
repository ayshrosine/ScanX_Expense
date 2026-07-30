
#category buckets 
CATEGORIES = [
    "food", "logistic", "drinks", "Travel",  "Grocery expense","Utilities", "Other"
]

def build_category_prompt(description_text:str) -> str:
    categroy_list = ",".join(CATEGORIES)
    return f"""

your are an expert classficaion agent. Your task is to analysze the following single service description and assign it to one of the predefined category.

#predefined categories:
{categroy_list}

#Instructions: 
- **STRICTLY** return ONLY the chosen category name as a single string. 
- If the description is vague or doesn't fit, choose "Other".
- The output MUST match one of the categories exactly.
- DO NOT return any quotes, explanation, or markdown.

---
Service Description to categorize : "{description_text}"

Category:"""