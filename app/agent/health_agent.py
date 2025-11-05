from agno.agent import Agent
from app.prompts import PROMPT_TEMPLATE, STEP_META, STEP_REMINDERS
from app.memory import SimpleMemory
import logging
from openai import OpenAI
import os
from agno.models.openai import OpenAIChat


user_steps = {}

api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)

def get_user_step(user_id: str) -> int:
    return user_steps.get(user_id, 1)


def build_prompt(user_input: str, user_id: str,step: int) -> str:
    purpose = STEP_META.get(str(step), "Continue supporting the user.")
    reminder = STEP_REMINDERS.get(str(step), "")

    prompt = PROMPT_TEMPLATE.format(
        step=step,
        purpose=purpose,
        user_input=user_input,
        reminder=reminder
    )
    return prompt

memory = SimpleMemory()

def format_step_meta():
    return "\n".join([f"{k}. {v}" for k, v in STEP_META.items()])



async def decide_step(user_input:str,user_id:str) ->int:
    previous_step =get_user_step(user_id)
    step_definition = format_step_meta()
    reasoning_prompt = f"""You're an expert agent helping guide users through a structured 8-step medical assistant conversation.
{step_definition}
Current user message: "{user_input}"
Previous step : {previous_step}

Determine the most appropriate step (1 to 8) that best matches what the user is expressing.
Only return a number from 1 to 8.
"""
    response = step_selector_agent.run(reasoning_prompt, user_id=user_id,memory=memory)
    try:
        step = int(response.content.strip())
        step = min(max(step, 1), 8)

    except:
        step = previous_step
    
    user_steps[user_id] = step
    return step

step_selector_agent = Agent(

    name="stepselector",
    role="Determine which step of the 8-step structured medical conversation is appropriate for the current user message. Only returen the number between 1 and 8",
    model=OpenAIChat(id="gpt-4o-mini"),
    # memory=memory
)

health_agent = Agent(
    
    name="Meera",
    role="A helpful assistant from a general practice clinic guiding users through a structured 8-step conversation.",
    model=OpenAIChat(id="gpt-4o-mini"),
    # memory=memory
)


# Agent runner
async def run_agent(agent: Agent, user_input: str, user_id: str) -> str:
    step = await decide_step(user_input,user_id)
    prompt = build_prompt(user_input, user_id,step) 
    response = agent.run(prompt, user_id=user_id, memory=memory)
    try:
        print(f"Input tokens: {agent.run_response.metrics['input_tokens']}")
        print(f"Output tokens: {agent.run_response.metrics['output_tokens']}")
        print(f"Total tokens: {agent.run_response.metrics['total_tokens']}")
    except Exception as e:
        print("Token usage not available from response:", e)
    return response.content, step
