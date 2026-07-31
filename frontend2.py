import streamlit as st
import pandas as pd
import sqlite3
from streamlit_dynamic_filters import DynamicFilters
from ollama3 import response_to_user_query

st.title("projects_with_suraj")
st.title("expense tracking table")


DB_NAME = "ocr_master.db"
TABLE_NAME = "ocr_line_items"

def load_data(): 
    try:
        con = sqlite3.connect(DB_NAME) 
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", con) 
        con.close() 
        return df
        
    except sqlite3.Error as e:
        st.error(f"Error loading data from database: {e}")
        # Return an empty DataFrame instead of None to prevent errors in st.dataframe
        return pd.DataFrame() 
    
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return pd.DataFrame()

# Load and display the data
data_df = load_data()


#adding filter
filters_obj= DynamicFilters(
    data_df,
    filters= ['Category','Invoice_No']
)

with st.sidebar:
    st.header("Filter Expenses")
    # 2. Display the filter widgets in the sidebar
    filters_obj.display_filters()

st.dataframe(filters_obj.filter_df(), use_container_width=True)

st.title("chat box")
user_question = st.chat_input("ask me anything")
if user_question:
    st.write(f"{user_question}")
    print(user_question)
    #converting userinputin to sql query
    sql_query_generation = response_to_user_query(user_question)
    print(sql_query_generation)

    #fetching information from table
    try:
        con = sqlite3.connect(DB_NAME)
        output = pd.read_sql_query(sql_query_generation,con)
        print(output)
        con.close()
        st.chat_message("assistance").dataframe(output)
    except Exception as e:
        print(f"error is {e}")
    


