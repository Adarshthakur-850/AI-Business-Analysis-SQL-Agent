from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

try:
    _default_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    _default_client = None

def explain_result(question: str, df: pd.DataFrame, api_key: str = None) -> str:
    client = _default_client
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
        except:
            pass

    if not client or not client.api_key:
        return "OpenAI API Key missing. Showing data only."
        
    if "error" in df.columns:
        return f"Query failed: {df['error'][0]}"
        
    # Truncate df string if too long
    df_str = df.head(10).to_string()
    
    prompt = f"""
    Question: {question}
    
    Data Result:
    {df_str}
    
    Explain this result in 2-3 sentences to a business user. Highlight key insights.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a business analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Could not generate explanation: {e}"
