from langchain.tools import tool
import httpx
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from composio_langchain import Action, ComposioToolSet

load_dotenv()

# Initialize Composio
composio_toolset = ComposioToolSet()
composio_tools = composio_toolset.get_tools(["GMAIL_SEND_EMAIL", "GOOGLECALENDAR_QUICK_ADD"])
# IRCTC Configuration
IRCTC_HEADERS = {
    'x-rapidapi-key': os.getenv("IRCTC_API_KEY"),
    'x-rapidapi-host': "irctc1.p.rapidapi.com"
}

STATION_CODES = {
    "delhi": "DEL", "mumbai": "BOM",
    "chennai": "MAS", "bangalore": "SBC"
}

# --- Core IRCTC Tools ---
@tool
def search_trains(source: str, destination: str, date: str) -> list:
    """Search trains between stations. Input can be city names or station codes."""
    source_code = STATION_CODES.get(source.lower(), source.upper()[:3])
    dest_code = STATION_CODES.get(destination.lower(), destination.upper()[:3])
    
    try:
        response = httpx.get(
            "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations",
            params={
                "fromStationCode": source_code,
                "toStationCode": dest_code,
                "dateOfJourney": date
            },
            headers=IRCTC_HEADERS
        )
        return response.json().get("data", [])
    except Exception as e:
        return [{"error": str(e)}]

@tool
def book_train_ticket(train_number: str, source: str, destination: str, 
                     date: str,email:str, passengers: list) -> dict:
    """Book a train ticket (simulated) and send confirmation."""
    booking_id = f"IRCTC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Simulate booking
    booking_details = {
        "status": "confirmed",
        "booking_id": booking_id,
        "train_number": train_number,
        "from": source,
        "to": destination,
        "date": date,
        "passengers": passengers
    }
    return booking_details

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Combine all tools
tools = [
    search_trains,
    book_train_ticket,
    *composio_tools  # Now properly initialized
]

# System prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an IRCTC assistant with these capabilities:
1. Search trains between stations
2. Book tickets (simulated)
3. Send email confirmations
4. Add trips to Google Calendar

For bookings, always:
- Confirm details with user
- Send email confirmation
- Add calendar event"""),
    ("human", "{input}"),
    ("ai","{agent_scratchpad}")
])

# Create agent
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)