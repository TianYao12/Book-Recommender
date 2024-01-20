import streamlit as st
import agent_example as backend

st.title("Chatbot")
st.write("This is a chatbot that answers your questions")

# Get user input
with st.sidebar:
    with st.form(key='user_input'):
        question = st.text_input("Question", max_chars=100)
        submit = st.form_submit_button("Submit")

# Get answer
if (question and submit):
    placeholder = st.empty()
    with placeholder:
        st.write("Running model. This may take some time.")
        answer = backend.get_answer(question)
        st.write("Answer: " + answer)