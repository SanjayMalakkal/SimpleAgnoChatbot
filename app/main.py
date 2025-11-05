import logging
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import re
import httpx
from app.agent.health_agent import user_steps, build_prompt, health_agent,get_user_step,run_agent


API_URL =""

# Load environment variables
load_dotenv()

app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/gp-bot/init")
async def init_bot(uuid: str):

    user_steps[uuid] = 1  

    initial_prompt = build_prompt("", uuid, step=1)
    response = health_agent.run(initial_prompt, user_id=uuid)

    return JSONResponse({
        "response": response.content,
        "step": 1,
        "end": False
    })


@app.post("/gp-bot")
async def gp_bot(uuid: str = Form(...), body: str = Form(...)):
    global user_steps
    user_input = body.strip()
    

    if not user_input:

        user_steps[uuid] = 1
        initial_prompt = build_prompt("", uuid, step=1)
        response = health_agent.run(initial_prompt, user_id=uuid)

        return JSONResponse({
            "response": response.content,
            "step": 1,
            "end": False
        })

    try:
        phone_match = re.fullmatch(r"(\+91)?[6-9]\d{9}", user_input)
        if re.fullmatch(r"\d{8,}", user_input) and not phone_match:
            return JSONResponse({
                "response": "Please enter a valid 10-digit Indian mobile number",
                "step": get_user_step(uuid),
                "end": False
        })
        if phone_match:
            
            phone_number = phone_match.group()
            await submit_Phone(uuid, phone_number)

            current_step = get_user_step(uuid)
            next_step = current_step +1
            user_steps[uuid] = next_step
            nextprompt = build_prompt("", uuid, step=next_step)
            response = health_agent.run(nextprompt,user_id=uuid)

            # return JSONResponse({
            #     "response": f"Thanks! Your phone number is {phone_number}.",
            #     "step": get_user_step(uuid),
            #     "end": False
            # })
      
        response, step= await run_agent(health_agent, user_input, uuid)
        # step = get_user_step(uuid)
        logger.info(f"[UUID: {uuid} | Step: {step} | Output: {response}]")

        return JSONResponse({
            "response": response,
            "step": step,
            "end": step == 8
        })

    except Exception as e:
        logger.exception("Error while processing user input")
        return JSONResponse({"error": "Internal server error."}, status_code=500)


async def submit_Phone(uuid: str, Phone_no: str)-> None:
    async with httpx.AsyncClient() as Client:
        resp = await Client.post(
            API_URL,
            json={"user_id": uuid, "Phone_no": Phone_no},

        )
        resp.raise_for_status()