# app.py - Streamlit frontend for HealthConnect using mailbox-enabled agents
import streamlit as st
import asyncio
from uagents import Model
from uagents.query import send_sync_message

# ✅ Agent IDs (replace with actual agent IDs printed in terminal if needed)
APPOINTMENT_AGENT_ID = "agent1qtlfxcc0hyqu8eylgvl82nak4kwdyzjg7gl0l74cxl5zqejpnwxrz9lmnje"  # From terminal
SYMPTOM_AGENT_ID     = "agent1qv2fzh42mjjsjw8kwed5c4supyc804ghylla3xfm9t7tunx4e44k23u9x68"
MEDICATION_AGENT_ID  = "agent1qw79p6rjdxpf9436f4lfe6dcw89ljrchy3pcc5fuysy6r77v8ndyqqc9eta"

# ✅ Message model (shared)
class Message(Model):
    query: str
    response: str = None

# ✅ Streamlit UI
st.set_page_config(page_title="HealthConnect", page_icon="🩺")
st.title("🩺 HealthConnect - Your AI Healthcare Assistant")

st.markdown("""
Enter your question or request below. Based on the type, it will be routed to:
- 🤒 Symptom Agent
- 💊 Medication Agent
- 📅 Appointment Agent

_All agents use the Fetch.ai ASI-1 LLM for intelligent responses._
""")

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

with st.form("query_form", clear_on_submit=True):
    user_input = st.text_input("Enter your health query:")
    submit = st.form_submit_button("Submit")

# ✅ Async-safe agent message sending
def send_to_agent(agent_id: str, query: str) -> str:
    async def _send():
        msg = Message(query=query)
        status = await send_sync_message(agent_id, msg, timeout=10)
        if hasattr(status, "message") and isinstance(status.message, Message):
            return status.message.response or "⚠️ Agent responded with no content."
        return "⚠️ Agent did not deliver a valid response."

    try:
        return asyncio.run(_send())
    except RuntimeError:
        return asyncio.get_event_loop().run_until_complete(_send())
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"

# ✅ Router based on keywords
def route_query(query: str) -> str:
    q = query.lower()

    if any(word in q for word in ["appointment", "book", "schedule", "reschedule"]):
        st.info("📅 Routing to Appointment Agent")
        return send_to_agent(APPOINTMENT_AGENT_ID, query)

    elif any(word in q for word in ["medication", "pill", "reminder", "take"]):
        st.info("💊 Routing to Medication Agent")
        return send_to_agent(MEDICATION_AGENT_ID, query)

    elif any(word in q for word in ["symptom", "pain", "cough", "fever", "headache", "feel", "sick", "cold", "throat", "nausea"]):
        st.info("🤒 Routing to Symptom Agent")
        return send_to_agent(SYMPTOM_AGENT_ID, query)

    else:
        st.info("🤖 Routing to Symptom Agent (fallback)")
        return send_to_agent(SYMPTOM_AGENT_ID, query)

# ✅ Handle submission
if submit and user_input:
    with st.spinner("Routing your query to the right agent..."):
        response = route_query(user_input)
        st.session_state.conversation.append(("You", user_input))
        st.session_state.conversation.append(("HealthConnect", response))

# ✅ Chat display
for speaker, message in reversed(st.session_state.conversation):
    st.markdown(f"**{speaker}:** {message}")
