import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8001/ask"

st.set_page_config(page_title="AI Business Analyst", layout="wide")

st.title("📊 AI Business Analysis Agent")
st.markdown("Ask questions about your business data in plain English.")

# Sidebar for schema info
with st.sidebar:
    st.subheader("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your key to enable AI features")
    
    st.subheader("Database Schema")
    st.markdown("""
    **Customers**: id, name, city, signup_date
    **Products**: id, name, category, price
    **Orders**: id, customer_id, product_id, amount, order_date
    """)
    
    st.info("Try: 'Total sales by city' or 'Top 5 spending customers'")

question = st.text_input("Enter your question:", "Which city has the highest sales?")

if st.button("Analyze"):
    if question:
        with st.spinner("Analyzing..."):
            try:
                payload = {"question": question}
                if api_key:
                    payload["api_key"] = api_key
                
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    
                    # 1. Explanation
                    st.success("Analysis Complete")
                    st.markdown(f"### 💡 Insight\n{result.get('explanation', 'No explanation')}")
                    
                    # 2. Data
                    st.markdown("### 📋 Data Result")
                    data = result.get('data', [])
                    if data:
                        df = pd.DataFrame(data)
                        st.dataframe(df)
                    else:
                        st.write("No data returned.")
                        
                    # 3. Technical Details (SQL)
                    with st.expander("See Generated SQL"):
                        st.code(result.get('sql_query', ''), language='sql')
                        
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
    else:
        st.warning("Please enter a question.")
