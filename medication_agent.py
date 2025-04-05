from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class Message(Model):
    query: str
    response: str = None

class ASIRequest(Model):
    query: str

class ASIResponse(Model):
    response: str

ASI_AGENT_ID = "agent1qvn0t4u5jeyewp9l544mykv639szuhq8dhmatrgfuwqphx20n8jn78m9paa"
PENDING_REQUESTS = {}

agent = Agent(
    name="HealthConnectMedicationAgent",
    seed="medication_seed_phrase",
    port=8004,
    endpoint=["http://localhost:8004/submit"],
    mailbox=True,
)

fund_agent_if_low(str(agent.wallet.address()))

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("💊 Medication Agent is live")

@agent.on_message(model=Message)
async def forward_to_asi(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"📨 User query: {msg.query}")
    PENDING_REQUESTS[msg.query] = sender
    await ctx.send(ASI_AGENT_ID, ASIRequest(query=msg.query))

@agent.on_message(model=ASIResponse)
async def handle_asi_response(ctx: Context, sender: str, msg: ASIResponse):
    for q in PENDING_REQUESTS:
        if q.lower() in msg.response.lower():
            await ctx.send(PENDING_REQUESTS[q], Message(query=q, response=msg.response))
            del PENDING_REQUESTS[q]
            break

if __name__ == "__main__":
    agent.run()
