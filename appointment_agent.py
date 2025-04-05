from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Message model
class Message(Model):
    query: str
    response: str = None

# ASI request/response models
class ASIRequest(Model):
    query: str

class ASIResponse(Model):
    response: str

# ASI-1 Mini Agent (LLM-powered)
ASI_AGENT_ID = "agent1qvn0t4u5jeyewp9l544mykv639szuhq8dhmatrgfuwqphx20n8jn78m9paa"

# Track query-to-sender mapping
PENDING_REQUESTS = {}

# Initialize Appointment Agent on port 8010
agent = Agent(
    name="HealthConnectAppointmentAgent",
    seed="appointment_seed_phrase",
    port=8010,
    endpoint=["http://localhost:8010/submit"],
    mailbox=True,
)

fund_agent_if_low(str(agent.wallet.address()))

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("📅 Appointment Agent is live")
    ctx.logger.info(f"🆔 Agent Address: {agent.address}")

@agent.on_message(model=Message)
async def forward_to_asi(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"📨 User query: {msg.query}")
    PENDING_REQUESTS[msg.query] = sender
    await ctx.send(ASI_AGENT_ID, ASIRequest(query=msg.query))

@agent.on_message(model=ASIResponse)
async def handle_asi_response(ctx: Context, sender: str, msg: ASIResponse):
    for q in list(PENDING_REQUESTS.keys()):
        if q.lower() in msg.response.lower():
            await ctx.send(PENDING_REQUESTS[q], Message(query=q, response=msg.response))
            ctx.logger.info(f"📤 Response sent for query: {q}")
            del PENDING_REQUESTS[q]
            break

if __name__ == "__main__":
    agent.run()
