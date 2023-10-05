
import os

import streamlit as st
# Add your own openai api key intstead of st.secrets . 
os.environ["OPENAI_API_KEY"] = st.secrets["api_key"]
OPENAI_API_KEY = st.secrets["api_key"]

import pandas as pd
import pandasai
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def display_output(output):
    # Displays the output from pandas-ai.

    if isinstance(output, str):
        st.write(output)
    elif isinstance(output, pd.DataFrame):
        st.dataframe(output)
    # elif isinstance(output, matplotlib.figure.Figure):
    #     # st.pyplot(output)
    #     image_path = os.path.join(os.getcwd(), "exports", "charts", "temp_chart.png")
    #     if os.path.exists(image_path):
    #         fig = plt.imread(image_path)
    #         st.image(fig)
    else:
        image_path = os.path.join(os.getcwd(), "exports", "charts", "temp_chart.png")
        if os.path.exists(image_path):
            fig = plt.imread(image_path)
            st.image(fig)
        st.write(output)
        
def ask_questions(pandas_ai, question):
    """Asks the user a question and returns the answer."""

    answer = pandas_ai.chat(question)
    return answer


if "questionsHistory" not in st.session_state:
    st.session_state.questionsHistory = []
def display_history():
    questions = st.session_state.get("questionsHistory", [])
    st.sidebar.subheader("History")
    for question in questions:
        st.sidebar.write(f"- {question}")
def display_output(output):
    """Displays the output from pandas-ai."""

    if isinstance(output, str):
        st.write(output)
    elif isinstance(output, pd.DataFrame):
        st.dataframe(output)
    elif isinstance(output, matplotlib.figure.Figure):
        # st.pyplot(output)
        fig = plt.figure(figsize=(8, 6),)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write(output)

def main():
    
    llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-16k")
    input_csvs = st.file_uploader("Upload your CSV files", type=['csv'], accept_multiple_files=True)
    if input_csvs:
        selected_file = st.selectbox("Select a CSV file", [file.name for file in input_csvs])
        selected_index = [file.name for file in input_csvs].index(selected_file)
        #load and display the selected csv file 
        st.info("CSV uploaded successfully")
        data = pd.read_csv(input_csvs[selected_index])
        pandas_ai = SmartDataframe(data, config={"llm": llm})
        # st.dataframe(data,use_container_width=True)
        #Enter the query for analysis
        st.info("Chat Below")
        input_text = st.text_area("Enter the query")
        # questionsHistory.append(input_text)
        if input_text:
            st.session_state.questionsHistory.append(input_text)
            display_output(answer)
        # #Perform analysis
        # if input_text:
        #     st.info("Your Query: "+ input_text)
        #     answer = ask_questions(pandas_ai, input_text)
        #     # result = chat_with_csv(data,input_text)
        #     # fig_number = plt.get_fignums()
        #     # if fig_number:
        #     #     st.pyplot(plt.gcf())
        #     # else:
        #     #     st.success(answer)
        #     display_output(answer)

    display_history()

if __name__ == "__main__":
    main()


