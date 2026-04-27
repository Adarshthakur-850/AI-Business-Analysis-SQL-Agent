from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Ensure we can import from agent/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

from agent import sql_generator, query_executor, explainer

app = FastAPI(title="AI SQL Agent")

class QueryRequest(BaseModel):
    question: str
    api_key: str = None

@app.post("/ask")
def ask_agent(request: QueryRequest):
    question = request.question
    api_key = request.api_key
    
    # 1. Generate SQL
    sql = sql_generator.generate_sql(question, api_key)
    
    # 2. Execute SQL
    df = query_executor.execute_query(sql)
    
    # 3. Explain
    explanation = explainer.explain_result(question, df, api_key)
    
    # Convert DF to dict for JSON response
    # Use 'records' orient for simple rows
    table_data = df.to_dict(orient="records")
    columns = list(df.columns)
    
    return {
        "question": question,
        "sql_query": sql,
        "data": table_data,
        "columns": columns,
        "explanation": explanation
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # Port 8001 to avoid conflict
