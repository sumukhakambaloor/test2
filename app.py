import streamlit as st
from openai import ChatCompletion
import json

# Load website content
with open("bmsit_data.json", "r") as file:
    website_data = json.load(file)

# Initialize chatbot memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chatbot function
def chatbot_response(question, memory):
    # Append question to the memory
    memory.append({"role": "user", "content": question})
    
    # Use website_data for domain-specific responses
    response = ""
    for key, value in website_data.items():
        if key.lower() in question.lower():
            response = value
            break
    
    # Fallback to OpenAI GPT (or other LLM)
    if not response:
        completion = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=memory
        )
        response = completion.choices[0].message["content"]
    
    # Append bot response to memory
    memory.append({"role": "assistant", "content": response})
    return response

# Streamlit interface
st.title("BMSIT Chatbot")
st.write("Ask me anything about BMSIT!")

user_input = st.text_input("Your question:")

if user_input:
    response = chatbot_response(user_input, st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.text_area("Chat History", value="\n".join([msg["content"] for msg in st.session_state.messages]), height=300)
