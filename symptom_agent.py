from uagents import Agent, Context, Model

class Message(Model):
    query: str
    response: str = None

class SymptomResponse(Model):
    response: str

class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str

ASI_AGENT_ID = "agent1qvn0t4u5jeyewp9l544mykv639szuhq8dhmatrgfuwqphx20n8jn78m9paa"
CLI_AGENT_ADDRESS = "agent1qv3dag4483k5dv4wkcncy65xpyrq4hgwk6nvuf0xzrhfz33cxaqj6xpg9c7"

agent = Agent(
    name="HealthConnectSymptomAgent",
    seed="symptom_seed_phrase",
    port=8003,
    endpoint=["http://localhost:8003/submit"],
    mailbox=True
)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("🤒 Symptom Agent is live")

async def prompting(query: str):
    return f"Based on the following symptoms, {query}, suggest possible causes and recommend next steps or actions the user should take, such as home remedies, consulting a doctor, or emergency care."

@agent.on_message(model=Message)
async def forward_to_asi(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"📨 User query: {msg.query}")
    prompt = await prompting(msg.query)
    await ctx.send(ASI_AGENT_ID, ASI1miniRequest(query=prompt))

@agent.on_message(model=ASI1miniResponse)
async def handle_asi_response(ctx: Context, sender: str, msg: ASI1miniResponse):
    await ctx.send(CLI_AGENT_ADDRESS, SymptomResponse(response=msg.response))

if __name__ == "__main__":
    agent.run()
