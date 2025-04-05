from uagents import Agent, Context, Model

# Shared message model for incoming requests
class Message(Model):
    query: str
    response: str = None

# Response model that will be sent back to the CLI
class AppointmentResponse(Model):
    response: str

# Model for ASI agent request and response
class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str

# Agent addresses
ASI_AGENT_ID = "agent1qvn0t4u5jeyewp9l544mykv639szuhq8dhmatrgfuwqphx20n8jn78m9paa"
CLI_AGENT_ADDRESS = "agent1qv3dag4483k5dv4wkcncy65xpyrq4hgwk6nvuf0xzrhfz33cxaqj6xpg9c7"

# Define the Appointment Agent
agent = Agent(
    name="HealthConnectAppointmentAgent",
    seed="appointment_seed_phrase",
    port=8010,
    endpoint=["http://localhost:8010/submit"],
    mailbox=True
)

# Log on startup
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("📅 Appointment Agent is live")

# Build the prompt to send to the ASI agent
async def prompting(query: str):
    return f"The user needs assistance with appointment-related tasks: {query}. Suggest helpful steps like scheduling, modifying, or canceling appointments."

# When a Message is received, send a query to the ASI agent
@agent.on_message(model=Message)
async def forward_to_asi(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"📨 User query: {msg.query}")
    prompt = await prompting(msg.query)
    await ctx.send(ASI_AGENT_ID, ASI1miniRequest(query=prompt))

# When the ASI agent responds, send the result back to the CLI agent
@agent.on_message(model=ASI1miniResponse)
async def handle_asi_response(ctx: Context, sender: str, msg: ASI1miniResponse):
    await ctx.send(CLI_AGENT_ADDRESS, AppointmentResponse(response=msg.response))

# Run the agent
if __name__ == "__main__":
    agent.run()
