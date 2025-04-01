from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Define a message model for incoming queries.
class Message(Model):
    query: str

# Initialize the Symptom Agent.
agent = Agent(
    name="HealthConnectSymptomAgent",
    seed="symptom_seed_phrase",  # Replace with a secure seed in production.
    port=8003,
    endpoint=["http://localhost:8003"]
)

# Fund the agent if its wallet balance is low.
fund_agent_if_low(str(agent.wallet.address()))

@agent.on_event("startup")
async def startup_function(ctx: Context):
    ctx.logger.info(f"Hello, I'm {agent.name} and I'm ready to check symptoms.")

# Handle incoming messages using the on_message decorator.
@agent.on_message(Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received query from {sender}: {msg.query}")
    response_text = (
        "Symptom Agent: Based on your symptoms, please monitor your condition and consider seeking professional advice if it worsens."
    )
    return {"response": response_text}

if __name__ == "__main__":
    agent.run()
