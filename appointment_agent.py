from uagents import Agent, Context, Model
import requests  # Changed from aiohttp to requests
from datetime import datetime, timedelta

class AppointmentRequest(Model):
    name: str
    email: str
    duration: int
    startTimeDate: str

class AppointmentResponse(Model):
    response: str

class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str


CAL_API_KEY = "cal_live_46843866d91e4e62cd54764b2fd96654"  
CAL_EVENT_ID = 2220111     
CAL_API_URL = "https://api.cal.com/v2/bookings"

agent = Agent()

asi_Address="agent1qvn0t4u5jeyewp9l544mykv639szuhq8dhmatrgfuwqphx20n8jn78m9paa"

async def book(name:str,email:str,duration:int,start:str ):
    payload = {
    "attendee": {
        "language": "en",
        "name": name,
        "timeZone": "Asia/Kolkata",
        "email": email
    },
    "start": start,
    "lengthInMinutes": duration,
    "eventTypeId": CAL_EVENT_ID,
    }
    headers = {
    "cal-api-version": "2024-08-13",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CAL_API_KEY}"
    }

    response = requests.request("POST", CAL_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()


@agent.on_message(model=AppointmentRequest)
async def startup(ctx: Context,sender:str, msg: AppointmentRequest):
    ctx.logger.info(f"Agent {agent.address} started.")
    ctx.storage.set("senderAddress", sender)
    ctx.storage.set("name", msg.name)
    ctx.storage.set("email", msg.email)
    ctx.storage.set("duration", msg.duration)
    ctx.logger.info(f"Agent {agent.address} received message: {msg}")
    ctx.logger.info(f"Agent {agent.address} received message: {msg.startTimeDate}")
    ctx.logger.info(f"Agent {agent.address} received message: {msg.duration}")
    ctx.logger.info(f"Agent {agent.address} received message: {msg.email}")
    await ctx.send(asi_Address, ASI1miniRequest(query=f"Extract the date and time from the following natural language string and return only the start time in ISO 8601 format in IST (e.g., '2025-04-10T16:00:00+05:30'), nothing else: {msg.startTimeDate}"))

@agent.on_message(model=ASI1miniResponse)
async def handle_asi_response(ctx: Context, sender: str, msg: ASI1miniResponse):
    ctx.logger.info(f"Received response from {sender}")
    start = msg.response
    name=ctx.storage.get("name")
    email=ctx.storage.get("email")
    duration=ctx.storage.get("duration")
    senderAddress = ctx.storage.get("senderAddress")
    response = await book(name,email,duration,start)
    if response:
        await ctx.send(senderAddress, AppointmentResponse(response=f"Appointment booked successfully for {name} on {email} for {duration} minutes"))
    else:
        await ctx.send(senderAddress, AppointmentResponse(response="Failed to book appointment"))



if __name__ == "__main__":
    agent.run()
