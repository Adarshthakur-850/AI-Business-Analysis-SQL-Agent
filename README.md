<<<<<<< HEAD
# AI Business Analysis SQL Agent

An AI-powered agent that converts natural language questions into SQL queries, executes them on a business database, and explains the results.

## Features
- **NL to SQL**: Converts "Who spent the most?" to `SELECT ...`.
- **Query Execution**: Runs safe `SELECT` queries on SQLite.
- **Explanation**: Explains the data insights in plain English.
- **API**: FastAPI backend.
- **UI**: Streamlit interface.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file and add your OpenAI API Key:
    ```
    OPENAI_API_KEY=sk-...
    ```

3.  **Initialize Database**:
    ```bash
    python database/create_db.py
    ```

4.  **Run API**:
    ```bash
    python -m uvicorn api.app:app --reload --port 8001
    ```

5.  **Run UI**:
    ```bash
    python -m streamlit run ui/streamlit_app.py
    ```

## Database Schema
- `customers`: id, name, city, signup_date
- `products`: id, name, category, price
- `orders`: id, customer_id, product_id, amount, order_date
=======
# AI-Business-Analysis-SQL-Agent
ml project
>>>>>>> a87cdfb1e9bfe2598fb6878f3f58058181974d40
