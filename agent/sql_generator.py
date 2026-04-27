from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client (Fallback to env)
try:
    _default_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    _default_client = None

# ... SCHEMA and SYSTEM_PROMPT ...

SCHEMA = """
Tables:
1. customers (id, name, city, signup_date)
2. products (id, name, category, price)
3. orders (id, customer_id, product_id, amount, order_date) - customer_id links to customers.id, product_id links to products.id
"""

SYSTEM_PROMPT = f"""
You are a SQL expert. Convert the user's natural language question into a VALID SQL query for SQLite.
Use the following schema:
{SCHEMA}

Rules:
1. Return ONLY the SQL query. No explanation, no markdown ticks.
2. Use standard SQLite syntax.
3. Be careful with joins.
4. If the question cannot be answered, return "SELECT 'I cannot answer that' as error".
"""

def generate_sql(question: str, api_key: str = None) -> str:
    client = _default_client
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
        except:
            pass
            
    if not client or not client.api_key:
        return "SELECT 'Error: OpenAI API Key missing' as error"
        
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            temperature=0
        )
        
        sql = response.choices[0].message.content.strip()
        # Clean potential markdown
        sql = sql.replace("```sql", "").replace("```", "").strip()
        return sql
    except Exception as e:
        return f"SELECT '{str(e)}' as error"
