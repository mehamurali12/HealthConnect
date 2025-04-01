# app.py
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os
import time
import requests

# Set your OpenAI API key (for your LLM usage)
os.environ['OPENAI_API_KEY'] = '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'
# Read your Fetch.ai API key from the environment
FETCHAI_API_KEY = os.getenv('eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjE3NDU5OTg5OTEsImlhdCI6MTc0MzQwNjk5MSwiaXNzIjoiZmV0Y2guYWkiLCJqdGkiOiJkYWZlN2JiOWQyMDc0MDllMTNjNGZlNDUiLCJzY29wZSI6ImF2Iiwic3ViIjoiZGM4YzE5OWFkYzBhYjRhNjJhMDM2M2QxZjk5NTZlZjc0MjIwNWViNTg3ZjM0MjAwIn0.kuBteY20emUxrYk60K_IclQ17_jBkdNZgj0EnVNfP6G_qVVLEQD-TUOzGz-37ZaCBQaNfLrSzmqKKykQsZ7hhmXRzapoY778XCQETgCek0WvvWp8zLGoQiXE7qw-HqqBL-OeB4vSCC5iE1r89hpkQOkCZ0L-w80J0ekyLCkm7r6Gg4vwvK6kFrRRWHOL4gdCaWzaUdavgDlJFXs4w9tI6Ab4NapWRvKjSWu3cmU0Dx-LGLBE4tC9O_JlUuSX-LzwO2kWd3QwpgIMv_tfaYQb7S4fwvYBZvBGMjl2brfAyIpg1WXoRr-rY1iRoeM7OKSEMLKIlhSG7XUnddaK7o1GVA')

# Define a prompt template for general health queries
prompt_template = """
You are HealthConnect, a friendly and knowledgeable healthcare assistant.
Your role is to provide medically specific guidance on general health concerns.
User Query: {user_input}
Remember: Provide clear, medically-informed responses that may include advice such as monitoring symptoms, over-the-counter suggestions, or recommendations to seek professional care when needed.
Always include a disclaimer that this information is for informational purposes only and is not a substitute for professional medical advice.
Response:
"""
template = PromptTemplate(input_variables=["user_input"], template=prompt_template)

# Initialize the LLM chain with ChatOpenAI
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
chain = LLMChain(llm=llm, prompt=template)

# Define common headers including your Fetch.ai API key if required by the endpoint
headers = {
    "Authorization": f"Bearer {FETCHAI_API_KEY}",
    "Content-Type": "application/json"
}

# Example endpoints: if you're connecting via Agentverse,
# replace these with the actual public URLs provided by Agentverse.
APPOINTMENT_AGENT_URL = "http://localhost:8001/submit"  # or the Agentverse URL
MEDICATION_AGENT_URL  = "http://localhost:8002/submit"
SYMPTOM_AGENT_URL     = "http://localhost:8003/submit"

def route_to_appointment_agent(user_input):
    st.info("Routing to HealthConnect Appointment Agent...")
    try:
        response = requests.post(APPOINTMENT_AGENT_URL, json={"query": user_input}, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("response", "No response from Appointment Agent")
        else:
            return f"Error: Received status code {response.status_code} from Appointment Agent."
    except Exception as e:
        return f"Error: {str(e)}"

def route_to_medication_agent(user_input):
    st.info("Routing to HealthConnect Medication Agent...")
    try:
        response = requests.post(MEDICATION_AGENT_URL, json={"query": user_input}, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("response", "No response from Medication Agent")
        else:
            return f"Error: Received status code {response.status_code} from Medication Agent."
    except Exception as e:
        return f"Error: {str(e)}"

def route_to_symptom_agent(user_input):
    st.info("Routing to HealthConnect Symptom Agent...")
    try:
        response = requests.post(SYMPTOM_AGENT_URL, json={"query": user_input}, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("response", "No response from Symptom Agent")
        else:
            return f"Error: Received status code {response.status_code} from Symptom Agent."
    except Exception as e:
        return f"Error: {str(e)}"

def process_query(user_input):
    lower_query = user_input.lower()
    if "appointment" in lower_query:
        return route_to_appointment_agent(user_input)
    elif "medication" in lower_query or "reminder" in lower_query:
        return route_to_medication_agent(user_input)
    elif "symptom" in lower_query:
        return route_to_symptom_agent(user_input)
    else:
        return chain.run(user_input=user_input)

def main():
    st.title("HealthConnect Healthcare Assistant")
    st.markdown(
        "**Disclaimer:** This bot provides medically informed guidance for general health concerns and scheduling convenience. It is not a substitute for professional medical advice."
    )

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your health query here:")
        submit_button = st.form_submit_button(label="Submit")

    if submit_button and user_input:
        with st.spinner("Processing your request..."):
            response = process_query(user_input)
        st.session_state.conversation.append(("user", user_input))
        st.session_state.conversation.append(("assistant", response))

    # Display the conversation history (most recent first)
    if hasattr(st, "chat_message"):
        for speaker, message in reversed(st.session_state.conversation):
            with st.chat_message(speaker):
                st.markdown(message)
    else:
        for speaker, message in reversed(st.session_state.conversation):
            st.markdown(f"**{speaker.title()}:** {message}")

if __name__ == "__main__":
    main()
