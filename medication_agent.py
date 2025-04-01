from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Define a message model for incoming queries.
class Message(Model):
    query: str

# Initialize the Medication Agent.
agent = Agent(
    name="HealthConnectMedicationAgent",
    seed="medication_seed_phrase",  # Replace with a secure seed in production.
    port=8002,
    endpoint=["http://localhost:8002"]
)

# Fund the agent if its wallet balance is low.
fund_agent_if_low(str(agent.wallet.address()))

@agent.on_event("startup")
async def startup_function(ctx: Context):
    ctx.logger.info(f"Hello, I'm {agent.name} and I'm ready to set medication reminders.")

# Handle incoming messages using the on_message decorator.
@agent.on_message(Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received query from {sender}: {msg.query}")
    response_text = "Medication Agent: Your medication reminder has been set for 8 AM daily."
    return {"response": response_text}

if __name__ == "__main__":
    agent.run()
