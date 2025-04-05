from uagents import Agent, Context, Model

class Message(Model):
    query: str
    response: str = None

class MedicationResponse(Model):
    response: str

class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str

ASI_AGENT_ID = "agent1qvn0t4u5jeyewp9l544mykv639szuhq8dhmatrgfuwqphx20n8jn78m9paa"
CLI_AGENT_ADDRESS = "agent1qv3dag4483k5dv4wkcncy65xpyrq4hgwk6nvuf0xzrhfz33cxaqj6xpg9c7"

agent = Agent(
    name="HealthConnectMedicationAgent",
    seed="medication_seed_phrase",
    port=8004,
    endpoint=["http://localhost:8004/submit"],
    mailbox=True
)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("💊 Medication Agent is live")

async def prompting(query: str):
    return f"Respond to the following user request about medication: {query}. Provide reminders, dosage info, or any safety suggestions as needed."

@agent.on_message(model=Message)
async def forward_to_asi(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"📨 User query: {msg.query}")
    prompt = await prompting(msg.query)
    await ctx.send(ASI_AGENT_ID, ASI1miniRequest(query=prompt))

@agent.on_message(model=ASI1miniResponse)
async def handle_asi_response(ctx: Context, sender: str, msg: ASI1miniResponse):
    await ctx.send(CLI_AGENT_ADDRESS, MedicationResponse(response=msg.response))

if __name__ == "__main__":
    agent.run()
