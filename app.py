from uagents import Agent, Context, Model
import asyncio

# Shared input message model
class Message(Model):
    query: str
    response: str = None

# Response models from other agents
class SymptomResponse(Model):
    response: str

class MedicationResponse(Model):
    response: str

class AppointmentResponse(Model):
    response: str

# Response queue
response_queue = asyncio.Queue()

# CLI Agent
cli_agent = Agent(
    name="CLIFrontendAgent",
    seed="cli_agent_seed_phrase",
    mailbox=True,
)

# Catch SymptomResponse
@cli_agent.on_message(model=SymptomResponse)
async def symptom_response(ctx: Context, sender: str, msg: SymptomResponse):
    await response_queue.put((sender, msg.response))

# Catch MedicationResponse
@cli_agent.on_message(model=MedicationResponse)
async def medication_response(ctx: Context, sender: str, msg: MedicationResponse):
    await response_queue.put((sender, msg.response))

# Catch AppointmentResponse
@cli_agent.on_message(model=AppointmentResponse)
async def appointment_response(ctx: Context, sender: str, msg: AppointmentResponse):
    await response_queue.put((sender, msg.response))

# Input prompt loop
@cli_agent.on_event("startup")
async def startup(ctx: Context):
    print("🩺 HealthConnect CLI is running!")
    print(f"Your agent address: {cli_agent.address}")
    print("Type your health query below (type 'exit' to quit):")

    while True:
        user_input = input("🧑 You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting CLI.")
            break

        target_agent = route_query(user_input)
        msg = Message(query=user_input)

        try:
            await ctx.send(target_agent, msg)
            print(f"📨 Sent message to {target_agent}. Waiting for response...\n")

            sender, response = await response_queue.get()
            print(f"📬 Received response from {sender}: {response}\n")

        except Exception as e:
            print(f"❌ Error sending message: {e}")

# Simple keyword-based router
def route_query(query: str) -> str:
    q = query.lower()
    if any(word in q for word in ["appointment", "book", "schedule"]):
        return "agent1qtlfxcc0hyqu8eylgvl82nak4kwdyzjg7gl0l74cxl5zqejpnwxrz9lmnje"
    elif any(word in q for word in ["medication", "pill", "reminder"]):
        return "agent1qw79p6rjdxpf9436f4lfe6dcw89ljrchy3pcc5fuysy6r77v8ndyqqc9eta"
    return "agent1qv2fzh42mjjsjw8kwed5c4supyc804ghylla3xfm9t7tunx4e44k23u9x68"

# Run it
if __name__ == "__main__":
    cli_agent.run()
