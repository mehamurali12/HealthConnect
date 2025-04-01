from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Define a message model for incoming queries.
class Message(Model):
    query: str

# Initialize the Appointment Agent.
agent = Agent(
    name="HealthConnectAppointmentAgent",
    seed="appointment_seed_phrase",  # Replace with a secure seed in production.
    port=8001,
    endpoint=["http://localhost:8001"]
)

# Fund the agent if its wallet balance is low.
fund_agent_if_low(str(agent.wallet.address()))

@agent.on_event("startup")
async def startup_function(ctx: Context):
    ctx.logger.info(f"Hello, I'm {agent.name} and I'm ready to schedule appointments.")

# Handle incoming messages using the on_message decorator.
@agent.on_message(Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received query from {sender}: {msg.query}")
    response_text = "Appointment Agent: I suggest scheduling an appointment at 3 PM tomorrow."
    return {"response": response_text}

if __name__ == "__main__":
    agent.run()
